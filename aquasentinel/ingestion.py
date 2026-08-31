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

# Illustrative classroom review bands only. They are deliberately retained as
# explainable educational checks and are not regulatory or operating limits.
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

INDICATOR_TERMS = (
    "unauthorized",
    "denied",
    "unexpected",
    "anomaly",
    "alarm",
    "failed",
    "failure",
    "timeout",
    "scada",
    "plc",
    "suricata",
    "zeek",
    "modbus",
    "chlorine",
    "turbidity",
    "conductivity",
    "pressure",
    "membrane",
)


@dataclass(frozen=True)
class ParsedDataset:
    filename: str
    format: str
    records: list[dict[str, Any]]


def _extension(filename: str) -> str:
    lowered = filename.lower()
    for extension in SUPPORTED_EXTENSIONS:
        if lowered.endswith(extension):
            return extension
    return ""


def _coerce(value: Any) -> Any:
    if value is None or isinstance(value, (int, float, bool)):
        return value
    text = str(value).strip()
    if not text:
        return ""
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return float(text) if any(ch in text for ch in ".eE") else int(text)
    except ValueError:
        return text


def _flatten_record(record: dict[str, Any]) -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    for key, value in record.items():
        clean_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                nested = str(nested_key).strip().lower().replace(" ", "_").replace("-", "_")
                flattened[f"{clean_key}_{nested}"] = _coerce(nested_value)
                flattened.setdefault(nested, _coerce(nested_value))
        else:
            flattened[clean_key] = _coerce(value)
    return flattened


def _parse_text_line(line: str, line_number: int) -> dict[str, Any]:
    record: dict[str, Any] = {"line": line_number, "message": line.rstrip()}
    for key, value in re.findall(r"([A-Za-z][A-Za-z0-9_.-]*)\s*[=:]\s*(\"[^\"]*\"|'[^']*'|[^,;\s]+)", line):
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
    detected = extension.lstrip(".")

    if extension == ".csv":
        reader = csv.DictReader(io.StringIO(content))
        if not reader.fieldnames:
            raise ValueError("CSV file does not contain a header row")
        records = [_flatten_record(dict(row)) for row in reader]
    elif extension == ".json":
        payload = json.loads(content)
        if isinstance(payload, list):
            records = [_flatten_record(item) if isinstance(item, dict) else {"value": _coerce(item)} for item in payload]
        elif isinstance(payload, dict):
            for candidate in ("records", "events", "data", "telemetry", "logs"):
                value = payload.get(candidate)
                if isinstance(value, list):
                    records = [_flatten_record(item) if isinstance(item, dict) else {"value": _coerce(item)} for item in value]
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
            records.append(_flatten_record(item) if isinstance(item, dict) else {"line": line_number, "value": _coerce(item)})
    else:
        records = [_parse_text_line(line, line_number) for line_number, line in enumerate(content.splitlines(), 1) if line.strip()]

    if not records:
        raise ValueError("No readable records were found")
    if len(records) > MAX_RECORDS:
        records = records[:MAX_RECORDS]
    return ParsedDataset(filename=filename, format=detected, records=records)


def _canonical_values(records: list[dict[str, Any]]) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {}
    for canonical, aliases in FIELD_ALIASES.items():
        series: list[float] = []
        for record in records:
            found: Any = None
            for alias in aliases:
                if alias in record:
                    found = record[alias]
                    break
            if isinstance(found, (int, float)) and not isinstance(found, bool):
                series.append(float(found))
        if series:
            values[canonical] = series
    return values


def _severity_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        explicit = str(record.get("severity", record.get("level", ""))).lower()
        if explicit:
            matched = False
            for word, severity in SEVERITY_WORDS.items():
                if word in explicit:
                    counts[severity] += 1
                    matched = True
                    break
            if matched:
                continue
        text = " ".join(str(value) for value in record.values()).lower()
        for word, severity in SEVERITY_WORDS.items():
            if re.search(rf"\b{re.escape(word)}\b", text):
                counts[severity] += 1
                break
        else:
            counts["unclassified"] += 1
    return counts


def _indicator_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        text = " ".join(str(value) for value in record.values()).lower()
        for term in INDICATOR_TERMS:
            if term in text:
                counts[term] += 1
    return counts


def _ml_anomalies(records: list[dict[str, Any]], metrics: dict[str, list[float]]) -> dict[str, Any]:
    usable = [name for name, values in metrics.items() if len(values) == len(records)]
    if len(records) < 12 or len(usable) < 2:
        return {
            "state": "NOT RUN",
            "detail": "Need at least 12 rows with two complete numeric telemetry fields",
            "anomaly_count": 0,
            "features": usable,
        }
    matrix = [[float(records[index][next(alias for alias in FIELD_ALIASES[name] if alias in records[index])]) for name in usable] for index in range(len(records))]
    model = IsolationForest(n_estimators=120, contamination="auto", random_state=133)
    predictions = model.fit_predict(matrix)
    anomaly_indexes = [index for index, prediction in enumerate(predictions) if prediction == -1]
    return {
        "state": "ANALYZED",
        "detail": "IsolationForest fitted to numeric fields in the loaded dataset",
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
        summary = {
            "count": len(values),
            "min": round(min(values), 3),
            "max": round(max(values), 3),
            "avg": round(fmean(values), 3),
            "last": round(values[-1], 3),
        }
        metric_summary[name] = summary
        band = CLASSROOM_BANDS.get(name)
        if band:
            low, high = band
            outside = sum(1 for value in values if (low is not None and value < low) or (high is not None and value > high))
            if outside:
                review_flags.append({"field": name, "outside_band": outside, "count": len(values), "band": [low, high]})

    severities = _severity_counts(records)
    indicators = _indicator_counts(records)
    ml = _ml_anomalies(records, metrics)

    risk_points = (
        severities.get("critical", 0) * 8
        + severities.get("error", 0) * 4
        + severities.get("warning", 0) * 2
        + sum(item["outside_band"] for item in review_flags) * 2
        + ml.get("anomaly_count", 0) * 2
    )
    risk_score = min(100, int(round(100 * risk_points / max(8, len(records) * 4))))
    decision = "REVIEW" if risk_score >= 35 or review_flags or severities.get("critical", 0) else "MONITOR"

    preview = []
    for index, record in enumerate(records[-12:], max(1, len(records) - 11)):
        preview.append({"index": index, "record": {key: record[key] for key in list(record)[:12]}})

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
        "indicators": dict(indicators.most_common(12)),
        "metrics": metric_summary,
        "review_flags": review_flags,
        "ml": ml,
        "recent_records": preview,
        "safety": "Local defensive analysis only. No control or write path to PLC, SCADA, dosing or utility infrastructure.",
        "note": "Water-quality bands are illustrative classroom review bands, not regulatory or operating limits.",
    }


def analyze_content(filename: str, content: str) -> dict[str, Any]:
    return analyze_dataset(parse_content(filename, content))
