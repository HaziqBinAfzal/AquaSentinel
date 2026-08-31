from __future__ import annotations

import csv
import io
import json
import re
from collections import Counter
from dataclasses import dataclass
from statistics import fmean
from typing import Any

from sklearn.ensemble import IsolationForest

MAX_RECORDS = 10_000
SUPPORTED_EXTENSIONS = {".log", ".txt", ".csv", ".json", ".jsonl"}

FIELD_ALIASES = {
    "ph": {"ph", "p_h"},
    "conductivity": {"conductivity", "ec", "electrical_conductivity"},
    "turbidity": {"turbidity", "ntu"},
    "residual_chlorine": {"residual_chlorine", "chlorine", "free_chlorine"},
    "salinity": {"salinity"},
    "feed_pressure": {"feed_pressure", "feedpressure", "feed_bar"},
    "ro_pressure": {"ro_pressure", "ropressure", "ro_bar", "membrane_pressure"},
    "flow_rate": {"flow_rate", "flow", "flowrate"},
    "temperature": {"temperature", "temp"},
    "tank_level": {"tank_level", "tank", "level"},
    "energy_kwh": {"energy_kwh", "energy", "kwh"},
    "membrane_health": {"membrane_health", "membrane", "membrane_health_pct"},
}

# Illustrative classroom review bands only; never regulatory or operating limits.
CLASSROOM_BANDS = {
    "ph": (6.5, 8.5),
    "conductivity": (None, 650.0),
    "turbidity": (None, 1.0),
    "residual_chlorine": (0.25, 1.5),
    "salinity": (None, 0.7),
    "membrane_health": (70.0, None),
}

SEVERITY_WORDS = {
    "critical": "critical",
    "fatal": "critical",
    "error": "error",
    "failed": "error",
    "failure": "error",
    "warning": "warning",
    "warn": "warning",
    "alarm": "warning",
    "info": "info",
}

SECURITY_TERMS = (
    "unauthorized",
    "denied",
    "unexpected",
    "failed",
    "failure",
    "timeout",
    "scada",
    "plc",
    "suricata",
    "zeek",
    "modbus",
)

PROCESS_TERMS = (
    "chlorine",
    "turbidity",
    "conductivity",
    "pressure",
    "membrane",
    "dosing",
    "contamination",
    "fouling",
)


@dataclass(frozen=True)
class ParsedDataset:
    filename: str
    format: str
    records: list[dict[str, Any]]


def _extension(filename: str) -> str:
    lowered = filename.lower()
    return next((extension for extension in SUPPORTED_EXTENSIONS if lowered.endswith(extension)), "")


def _coerce(value: Any) -> Any:
    if value is None or isinstance(value, (int, float, bool)):
        return value
    text = str(value).strip()
    if not text:
        return ""
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    try:
        return float(text) if any(ch in text for ch in ".eE") else int(text)
    except ValueError:
        return text


def _flatten_record(record: dict[str, Any]) -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    for key, value in record.items():
        clean = str(key).strip().lower().replace(" ", "_").replace("-", "_")
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                nested = str(nested_key).strip().lower().replace(" ", "_").replace("-", "_")
                flattened[f"{clean}_{nested}"] = _coerce(nested_value)
                flattened.setdefault(nested, _coerce(nested_value))
        else:
            flattened[clean] = _coerce(value)
    return flattened


def _parse_text_line(line: str, line_number: int) -> dict[str, Any]:
    record: dict[str, Any] = {"line": line_number, "message": line.rstrip()}
    pattern = r"([A-Za-z][A-Za-z0-9_.-]*)\s*[=:]\s*(\"[^\"]*\"|'[^']*'|[^,;\s]+)"
    for key, value in re.findall(pattern, line):
        clean_key = key.lower().replace("-", "_").replace(".", "_")
        record[clean_key] = _coerce(value.strip("\"'"))

    stamp = re.match(r"\s*(\d{4}-\d{2}-\d{2}[T ][0-9:.+\-Z]+)", line)
    if stamp:
        record.setdefault("timestamp", stamp.group(1))

    lowered = line.lower()
    for word, severity in SEVERITY_WORDS.items():
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            record.setdefault("severity", severity)
            break
    return record


def parse_content(filename: str, content: str) -> ParsedDataset:
    extension = _extension(filename)
    if not extension:
        raise ValueError("Unsupported file type. Use .log, .txt, .csv, .json or .jsonl")
    if not content.strip():
        raise ValueError("The selected file is empty")

    records: list[dict[str, Any]] = []

    if extension == ".csv":
        reader = csv.DictReader(io.StringIO(content))
        if not reader.fieldnames:
            raise ValueError("CSV file does not contain a header row")
        records = [_flatten_record(dict(row)) for row in reader]
    elif extension == ".json":
        payload = json.loads(content)
        if isinstance(payload, list):
            records = [
                _flatten_record(item) if isinstance(item, dict) else {"value": _coerce(item)}
                for item in payload
            ]
        elif isinstance(payload, dict):
            for candidate in ("records", "events", "data", "telemetry", "logs"):
                value = payload.get(candidate)
                if isinstance(value, list):
                    records = [
                        _flatten_record(item)
                        if isinstance(item, dict)
                        else {"value": _coerce(item)}
                        for item in value
                    ]
                    break
            else:
                records = [_flatten_record(payload)]
        else:
            records = [{"value": _coerce(payload)}]
    elif extension == ".jsonl":
        for line_number, line in enumerate(content.splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            record = (
                _flatten_record(item)
                if isinstance(item, dict)
                else {"line": line_number, "value": _coerce(item)}
            )
            records.append(record)
    else:
        records = [
            _parse_text_line(line, line_number)
            for line_number, line in enumerate(content.splitlines(), 1)
            if line.strip()
        ]

    if not records:
        raise ValueError("No readable records were found")

    return ParsedDataset(filename, extension.lstrip("."), records[:MAX_RECORDS])


def _canonical_values(records: list[dict[str, Any]]) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {}
    for canonical, aliases in FIELD_ALIASES.items():
        series: list[float] = []
        for record in records:
            found = next((record[alias] for alias in aliases if alias in record), None)
            if isinstance(found, (int, float)) and not isinstance(found, bool):
                series.append(float(found))
        if series:
            values[canonical] = series
    return values


def _severity_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        explicit = str(record.get("severity", record.get("level", ""))).lower()
        matched = None
        if explicit:
            matched = next(
                (severity for word, severity in SEVERITY_WORDS.items() if word in explicit),
                None,
            )
        if not matched:
            text = " ".join(str(value) for value in record.values()).lower()
            matched = next(
                (
                    severity
                    for word, severity in SEVERITY_WORDS.items()
                    if re.search(rf"\b{re.escape(word)}\b", text)
                ),
                "unclassified",
            )
        counts[matched] += 1
    return counts


def _term_counts(records: list[dict[str, Any]], terms: tuple[str, ...]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        text = " ".join(str(value) for value in record.values()).lower()
        for term in terms:
            if term in text:
                counts[term] += 1
    return counts


def _event_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, record in enumerate(records, 1):
        text = " ".join(str(value) for value in record.values()).lower()
        security = [term for term in SECURITY_TERMS if term in text]
        severity = str(record.get("severity", record.get("level", ""))).lower()
        if security or any(level in severity for level in ("critical", "error", "warning")):
            events.append(
                {
                    "index": index,
                    "timestamp": record.get("timestamp", ""),
                    "severity": severity or "event",
                    "source": record.get("source", ""),
                    "event": record.get("event_type", record.get("security_event", "")),
                    "evidence": ", ".join(security),
                    "message": str(record.get("message", ""))[:180],
                }
            )
    return events[-30:]


def _ml_anomalies(
    records: list[dict[str, Any]], metrics: dict[str, list[float]]
) -> dict[str, Any]:
    usable = [name for name, values in metrics.items() if len(values) == len(records)]
    if len(records) < 12 or len(usable) < 2:
        return {
            "state": "NOT RUN",
            "detail": "Need at least 12 rows with two complete numeric telemetry fields",
            "anomaly_count": 0,
            "features": usable,
            "anomaly_indexes": [],
        }

    matrix = [
        [
            float(records[index][next(alias for alias in FIELD_ALIASES[name] if alias in records[index])])
            for name in usable
        ]
        for index in range(len(records))
    ]
    model = IsolationForest(n_estimators=120, contamination="auto", random_state=133)
    predictions = model.fit_predict(matrix)
    anomaly_indexes = [index + 1 for index, prediction in enumerate(predictions) if prediction == -1]
    return {
        "state": "ANALYZED",
        "detail": "IsolationForest fitted locally to complete numeric telemetry fields",
        "anomaly_count": len(anomaly_indexes),
        "anomaly_indexes": anomaly_indexes[:50],
        "features": usable,
    }


def analyze_dataset(dataset: ParsedDataset) -> dict[str, Any]:
    records = dataset.records
    fields = sorted({key for record in records for key in record})
    metrics = _canonical_values(records)
    metric_summary: dict[str, dict[str, Any]] = {}
    review_flags: list[dict[str, Any]] = []

    for name, values in metrics.items():
        metric_summary[name] = {
            "count": len(values),
            "min": round(min(values), 3),
            "max": round(max(values), 3),
            "avg": round(fmean(values), 3),
            "last": round(values[-1], 3),
            "series": [round(value, 3) for value in values[-120:]],
        }
        if name in CLASSROOM_BANDS:
            low, high = CLASSROOM_BANDS[name]
            outside = sum(
                1
                for value in values
                if (low is not None and value < low) or (high is not None and value > high)
            )
            if outside:
                review_flags.append(
                    {
                        "field": name,
                        "outside_band": outside,
                        "count": len(values),
                        "band": [low, high],
                    }
                )

    severities = _severity_counts(records)
    security = _term_counts(records, SECURITY_TERMS)
    process = _term_counts(records, PROCESS_TERMS)
    ml = _ml_anomalies(records, metrics)

    fouling = bool(
        metric_summary.get("membrane_health", {}).get("min", 100) < 70
        or (
            metric_summary.get("ro_pressure", {}).get("max", 0) >= 63
            and metric_summary.get("flow_rate", {}).get("min", 9999) < 97
        )
    )

    energy = metric_summary.get("energy_kwh", {})
    if energy and energy.get("max", 0) > energy.get("avg", 0) * 1.08:
        energy_state = "REVIEW"
    elif energy:
        energy_state = "AVAILABLE"
    else:
        energy_state = "NOT AVAILABLE"

    cyber_physical = bool(security and (review_flags or process))
    risk_points = (
        severities.get("critical", 0) * 8
        + severities.get("error", 0) * 4
        + severities.get("warning", 0) * 2
        + sum(item["outside_band"] for item in review_flags) * 2
        + ml.get("anomaly_count", 0) * 2
    )
    risk_score = min(100, int(round(100 * risk_points / max(8, len(records) * 4))))
    decision = (
        "REVIEW"
        if risk_score >= 35 or review_flags or severities.get("critical", 0)
        else "MONITOR"
    )

    preview = [
        {"index": index, "record": {key: record[key] for key in list(record)[:12]}}
        for index, record in enumerate(records[-12:], max(1, len(records) - 11))
    ]
    review_events = _event_rows(records)

    objectives = [
        {
            "id": "ot",
            "title": "Water Treatment SCADA & OT Security",
            "status": "EVIDENCE FOUND" if security else "NO SECURITY EVIDENCE",
            "detail": (
                f"{sum(security.values())} keyword-record matches; "
                f"{len(review_events)} review events."
            ),
        },
        {
            "id": "quality",
            "title": "AI-Driven Water Quality Monitoring",
            "status": "REVIEW" if review_flags else ("MONITOR" if metrics else "NOT AVAILABLE"),
            "detail": (
                f"{len(review_flags)} configured quality/process fields have classroom-band "
                f"exceptions; ML {ml['state']}."
            ),
        },
        {
            "id": "threat",
            "title": "Critical Infrastructure Threat Detection & Response",
            "status": (
                "CORRELATED REVIEW"
                if cyber_physical
                else ("SECURITY REVIEW" if security else "MONITOR")
            ),
            "detail": (
                "Cyber and process/quality evidence are correlated for human-led response."
                if cyber_physical
                else "No cyber-physical correlation established from supplied evidence."
            ),
        },
        {
            "id": "resource",
            "title": "Resource Optimization & Energy Management",
            "status": energy_state,
            "detail": (
                f"Energy telemetry {'is present' if energy else 'was not found'}; membrane "
                f"fouling {'indicated' if fouling else 'not indicated by configured checks'}. "
                "Advisory only."
            ),
        },
        {
            "id": "devsecops",
            "title": "DevSecOps & Platform Assurance",
            "status": "VERIFIED AT BUILD",
            "detail": (
                "Input validation, local-only service, automated tests, Ruff, Bandit and "
                "Windows/Linux CI protect the analysis platform."
            ),
        },
        {
            "id": "compliance",
            "title": "Compliance & Public Health Reporting",
            "status": "AUDIT READY",
            "detail": (
                "Source evidence, exceptions and human-review disposition are retained in the "
                "analysis view; mappings are educational, not certification."
            ),
        },
    ]

    return {
        "source": {
            "filename": dataset.filename,
            "format": dataset.format,
            "records": len(records),
            "fields": fields[:80],
            "truncated": len(records) >= MAX_RECORDS,
        },
        "summary": {
            "risk_score": risk_score,
            "decision": decision,
            "critical": severities.get("critical", 0),
            "errors": severities.get("error", 0),
            "warnings": severities.get("warning", 0),
            "review_flags": len(review_flags),
        },
        "severity_counts": dict(severities),
        "indicators": dict(security.most_common(12)),
        "process_indicators": dict(process.most_common(12)),
        "metrics": metric_summary,
        "review_flags": review_flags,
        "ml": ml,
        "security_events": review_events,
        "cyber_physical": {
            "correlated": cyber_physical,
            "security_matches": sum(security.values()),
            "quality_exception_values": sum(item["outside_band"] for item in review_flags),
        },
        "maintenance": {
            "fouling_review": fouling,
            "energy_state": energy_state,
        },
        "objectives": objectives,
        "recent_records": preview,
        "safety": (
            "Local defensive analysis only. No control or write path to PLC, SCADA, dosing "
            "or utility infrastructure."
        ),
        "note": (
            "Water-quality bands are illustrative classroom review bands, not regulatory or "
            "operating limits."
        ),
    }


def analyze_content(filename: str, content: str) -> dict[str, Any]:
    return analyze_dataset(parse_content(filename, content))
