"""Schema-driven, read-only evidence analysis for AquaSentinel."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

SUPPORTED_SUFFIXES = {".csv", ".json", ".jsonl", ".xlsx"}
DOMAIN_HINTS = {
    "SCADA / OT": {"scada", "plc", "rtu", "hmi", "protocol", "network", "command", "valve", "pump", "setpoint", "control"},
    "WATER QUALITY": {"ph", "turbidity", "chlorine", "conductivity", "tds", "salinity", "quality", "contamination", "permeate"},
    "DESALINATION / PROCESS": {"membrane", "ro", "pressure", "flow", "recovery", "fouling", "feed", "brine", "temperature", "train"},
    "ENERGY / RESOURCE": {"energy", "power", "kwh", "efficiency", "demand", "consumption", "resource", "recovery"},
    "MAINTENANCE / ASSET": {"maintenance", "asset", "health", "condition", "failure", "workorder", "inspection", "service"},
    "ACCESS / IDENTITY": {"user", "identity", "badge", "access", "login", "role", "failed", "mfa", "operator"},
    "COMPLIANCE / AUDIT": {"audit", "compliance", "approval", "change", "policy", "control", "evidence", "review", "record"},
}
TIME_HINTS = {"timestamp", "time", "datetime", "date", "eventtime", "observed", "created", "recorded"}


def _tokens(value: str) -> set[str]:
    return {p for p in re.split(r"[^a-z0-9]+", value.lower()) if p}


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool): return None
    try:
        text = str(value).strip().replace(",", "")
        if not text: return None
        number = float(text)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError): return None


def _parse_time(value: Any) -> datetime | None:
    if value is None or str(value).strip() == "": return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip().replace("Z", "+00:00")
        try: dt = datetime.fromisoformat(text)
        except ValueError: return None
    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    return digest.hexdigest()


@dataclass
class EvidenceFile:
    path: str; name: str; file_type: str; rows: int; columns: list[str]; domain: str; confidence: float
    domain_scores: dict[str, float] = field(default_factory=dict)
    numeric_features: list[str] = field(default_factory=list)
    missing_cells: int = 0; total_cells: int = 0; anomaly_score: float = 0.0; anomaly_flags: int = 0; analyzed_rows: int = 0
    notes: list[str] = field(default_factory=list)
    sha256: str = ""; timestamp_field: str | None = None; time_start: str | None = None; time_end: str | None = None
    analysis_method: str = "schema-only"
    @property
    def missing_pct(self) -> float: return (100.0 * self.missing_cells / self.total_cells) if self.total_cells else 0.0


@dataclass
class EvidencePackage:
    datasets: list[EvidenceFile]; risk_score: float; risk_level: str; correlations: list[str] = field(default_factory=list)
    @property
    def total_rows(self) -> int: return sum(item.rows for item in self.datasets)
    @property
    def total_flags(self) -> int: return sum(item.anomaly_flags for item in self.datasets)


def _read_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle: return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list): return [dict(row) for row in data if isinstance(row, dict)]
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list) and all(isinstance(row, dict) for row in value): return [dict(row) for row in value]
            return [data]
    if suffix == ".jsonl":
        rows=[]
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                value=json.loads(line)
                if isinstance(value, dict): rows.append(value)
        return rows
    if suffix == ".xlsx":
        from openpyxl import load_workbook
        workbook=load_workbook(path, read_only=True, data_only=True); sheet=workbook.active; values=sheet.iter_rows(values_only=True)
        header=[str(v).strip() if v is not None else "" for v in next(values, ())]
        return [{header[i]: value for i,value in enumerate(row) if i < len(header) and header[i]} for row in values]
    raise ValueError(f"Unsupported evidence type: {suffix}")


def _infer_domain(columns: list[str]) -> tuple[str,float,dict[str,float]]:
    tokens=set().union(*(_tokens(c) for c in columns)) if columns else set(); scores={}
    for domain,hints in DOMAIN_HINTS.items():
        matches=len(tokens & hints); scores[domain]=min(1.0,matches/3.0) if matches else 0.0
    domain=max(scores,key=scores.get) if scores else "GENERAL / UNKNOWN"; confidence=scores.get(domain,0.0)
    return (domain,confidence,scores) if confidence else ("GENERAL / UNKNOWN",0.0,scores)


def _infer_timestamp(rows: list[dict[str,Any]], columns: list[str]) -> tuple[str|None,str|None,str|None]:
    best=None; best_values=[]; best_ratio=0.0
    for column in columns:
        hint=bool(_tokens(column) & TIME_HINTS); parsed=[_parse_time(r.get(column)) for r in rows]; values=[v for v in parsed if v]
        ratio=len(values)/len(rows) if rows else 0.0
        if values and ratio >= 0.6 and (hint or ratio > best_ratio): best,best_values,best_ratio=column,values,ratio
    if not best: return None,None,None
    return best,min(best_values).isoformat(),max(best_values).isoformat()


def _discover_numeric(rows,columns):
    usable=[]
    for column in columns:
        present=[v for v in (_as_float(r.get(column)) for r in rows) if v is not None]
        if len(present)<max(5,int(len(rows)*0.6)) or len(set(present))<2: continue
        if _tokens(column) & {"id","identifier","timestamp","time","date"}: continue
        if len(set(present))/max(1,len(present)) > 0.98 and any(t in _tokens(column) for t in {"number","code","sequence","index"}): continue
        usable.append(column)
    return usable


def _robust_anomaly(matrix: list[list[float]]) -> tuple[float,int]:
    array=np.asarray(matrix,dtype=float); med=np.median(array,axis=0); mad=np.median(np.abs(array-med),axis=0); mad=np.where(mad<1e-9,1.0,mad)
    row_scores=np.max(0.6745*np.abs(array-med)/mad,axis=1); flags=int(np.sum(row_scores>3.5)); pressure=min(100.0,float(np.percentile(row_scores,90))/7.0*100.0)
    return round(pressure,1),flags


def analyze_file(path: str|Path) -> EvidenceFile:
    evidence_path=Path(path).expanduser().resolve()
    if not evidence_path.is_file(): raise FileNotFoundError(evidence_path)
    if evidence_path.suffix.lower() not in SUPPORTED_SUFFIXES: raise ValueError(f"Unsupported evidence type: {evidence_path.suffix}")
    rows=_read_rows(evidence_path); columns=list(dict.fromkeys(k for r in rows for k in r.keys())); domain,confidence,scores=_infer_domain(columns)
    numeric=_discover_numeric(rows,columns); total=len(rows)*len(columns); missing=sum(1 for r in rows for c in columns if r.get(c) in (None,""))
    ts,start,end=_infer_timestamp(rows,columns)
    result=EvidenceFile(str(evidence_path),evidence_path.name,evidence_path.suffix.lower(),len(rows),columns,domain,confidence,scores,numeric,missing,total,sha256=_sha256(evidence_path),timestamp_field=ts,time_start=start,time_end=end)
    if not rows: result.notes.append("No records were available for analysis."); return result
    if not numeric: result.notes.append("No suitable numeric features were discovered; schema profiling only."); return result
    matrix=[]
    for row in rows:
        vector=[_as_float(row.get(c)) for c in numeric]
        if all(v is not None for v in vector): matrix.append(vector)
    result.analyzed_rows=len(matrix)
    if len(matrix)<5: result.notes.append("Too few complete numeric records for a defensible anomaly finding."); return result
    if len(matrix)<20:
        result.anomaly_score,result.anomaly_flags=_robust_anomaly(matrix); result.analysis_method="robust-MAD"
    else:
        scaled=StandardScaler().fit_transform(matrix); model=IsolationForest(n_estimators=160,contamination="auto",random_state=133); predictions=model.fit_predict(scaled); raw=-model.score_samples(scaled)
        low,high=float(min(raw)),float(max(raw)); normalized=sorted(100.0*(float(v)-low)/(high-low) if high>low else 0.0 for v in raw); idx=max(0,min(len(normalized)-1,math.ceil(.90*len(normalized))-1))
        result.anomaly_score=round(normalized[idx],1); result.anomaly_flags=sum(1 for v in predictions if v==-1); result.analysis_method="IsolationForest"
    result.notes.append("Anomaly indicators are not proof of contamination, compromise, or unsafe water."); return result


def _time_correlations(datasets: list[EvidenceFile]) -> list[str]:
    findings=[]
    timed=[d for d in datasets if d.time_start and d.time_end]
    for i,left in enumerate(timed):
        for right in timed[i+1:]:
            ls,le=datetime.fromisoformat(left.time_start),datetime.fromisoformat(left.time_end); rs,re=datetime.fromisoformat(right.time_start),datetime.fromisoformat(right.time_end)
            start=max(ls,rs); end=min(le,re)
            if start<=end: findings.append(f"{left.name} ↔ {right.name}: overlapping UTC evidence window {start.isoformat()} to {end.isoformat()}")
    return findings


def analyze_package(paths: list[str|Path]) -> EvidencePackage:
    datasets=[analyze_file(path) for path in paths]; weighted=[(d.anomaly_score,d.analyzed_rows or d.rows) for d in datasets if d.rows]; denominator=sum(w for _,w in weighted)
    risk=round(sum(s*w for s,w in weighted)/denominator,1) if denominator else 0.0; level="NORMAL" if risk<40 else "ELEVATED" if risk<70 else "HIGH"
    return EvidencePackage(datasets,risk,level,_time_correlations(datasets))
