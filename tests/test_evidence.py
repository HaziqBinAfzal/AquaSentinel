import csv
import hashlib

from aquasentinel.evidence import analyze_package
from aquasentinel.evidence_report import build_report


def _write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader(); writer.writerows(rows)


def test_domain_inference_does_not_depend_on_filename(tmp_path):
    path=tmp_path/"random_upload_73.csv"; rows=[{"sample":i,"ph":7+i*.001,"turbidity":.2+i*.01,"chlorine":.5+i*.002} for i in range(30)]; _write_csv(path,list(rows[0]),rows)
    result=analyze_package([path]); assert result.datasets[0].domain=="WATER QUALITY"; assert result.datasets[0].analyzed_rows==30; assert result.datasets[0].analysis_method=="IsolationForest"


def test_unknown_schema_falls_back_safely(tmp_path):
    path=tmp_path/"anything.csv"; rows=[{"alpha":str(i),"label":f"x-{i}"} for i in range(10)]; _write_csv(path,list(rows[0]),rows)
    result=analyze_package([path]); assert result.datasets[0].domain=="GENERAL / UNKNOWN"; assert result.datasets[0].anomaly_flags==0


def test_varying_file_count_and_order(tmp_path):
    water=tmp_path/"a.csv"; energy=tmp_path/"b.csv"; water_rows=[{"ph":7+i/1000,"conductivity":500+i} for i in range(25)]; energy_rows=[{"energy_kwh":100+i,"efficiency":80+i/10,"demand":90+i} for i in range(25)]
    _write_csv(water,list(water_rows[0]),water_rows); _write_csv(energy,list(energy_rows[0]),energy_rows); result=analyze_package([energy,water]); assert len(result.datasets)==2; assert {i.domain for i in result.datasets}=={"ENERGY / RESOURCE","WATER QUALITY"}


def test_sha256_provenance_matches_file(tmp_path):
    path=tmp_path/"proof.csv"; rows=[{"ph":7+i*.01,"turbidity":.1+i*.01} for i in range(8)]; _write_csv(path,list(rows[0]),rows)
    item=analyze_package([path]).datasets[0]; assert item.sha256==hashlib.sha256(path.read_bytes()).hexdigest(); assert len(item.sha256)==64


def test_small_dataset_uses_robust_method(tmp_path):
    path=tmp_path/"small.csv"; rows=[{"flow":100+i,"pressure":50+i*.2,"membrane_health":90-i} for i in range(10)]; _write_csv(path,list(rows[0]),rows)
    item=analyze_package([path]).datasets[0]; assert item.analysis_method=="robust-MAD"; assert item.analyzed_rows==10


def test_too_few_records_do_not_invent_model_finding(tmp_path):
    path=tmp_path/"tiny.csv"; rows=[{"ph":7+i*.1,"turbidity":.2+i*.1} for i in range(4)]; _write_csv(path,list(rows[0]),rows)
    item=analyze_package([path]).datasets[0]; assert item.analysis_method=="schema-only"; assert item.anomaly_score==0; assert item.anomaly_flags==0


def test_timestamp_inference_and_overlap(tmp_path):
    first=tmp_path/"first.csv"; second=tmp_path/"second.csv"
    a=[{"observed_at":f"2026-09-01T10:{i:02d}:00Z","ph":7+i*.01,"turbidity":.2+i*.01} for i in range(10)]
    b=[{"event_time":f"2026-09-01T10:{i+5:02d}:00Z","flow":100+i,"pressure":50+i} for i in range(10)]
    _write_csv(first,list(a[0]),a); _write_csv(second,list(b[0]),b); result=analyze_package([first,second])
    assert result.datasets[0].timestamp_field=="observed_at"; assert result.datasets[1].timestamp_field=="event_time"; assert len(result.correlations)==1


def test_non_overlapping_time_windows_do_not_claim_correlation(tmp_path):
    first=tmp_path/"one.csv"; second=tmp_path/"two.csv"
    a=[{"timestamp":f"2026-09-01T10:{i:02d}:00Z","ph":7+i*.01} for i in range(6)]; b=[{"timestamp":f"2026-09-02T10:{i:02d}:00Z","energy_kwh":100+i} for i in range(6)]
    _write_csv(first,list(a[0]),a); _write_csv(second,list(b[0]),b); assert analyze_package([first,second]).correlations==[]


def test_report_contains_provenance_and_safety_language(tmp_path):
    path=tmp_path/"report.csv"; rows=[{"ph":7+i*.01,"chlorine":.5+i*.01} for i in range(8)]; _write_csv(path,list(rows[0]),rows); package=analyze_package([path]); text=build_report(package)
    assert package.datasets[0].sha256 in text; assert "not proof of contamination" in text; assert "does not connect to or control PLCs" in text
