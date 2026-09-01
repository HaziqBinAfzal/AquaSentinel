import csv

from aquasentinel.evidence import analyze_package


def _write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def test_domain_inference_does_not_depend_on_filename(tmp_path):
    path = tmp_path / "random_upload_73.csv"
    rows = [{"sample": i, "ph": 7 + i * 0.001, "turbidity": 0.2 + i * 0.01, "chlorine": 0.5 + i * 0.002} for i in range(30)]
    _write_csv(path, list(rows[0]), rows)
    result = analyze_package([path])
    assert result.datasets[0].domain == "WATER QUALITY"
    assert result.datasets[0].analyzed_rows == 30


def test_unknown_schema_falls_back_safely(tmp_path):
    path = tmp_path / "anything.csv"
    rows = [{"alpha": str(i), "label": f"x-{i}"} for i in range(10)]
    _write_csv(path, list(rows[0]), rows)
    result = analyze_package([path])
    assert result.datasets[0].domain == "GENERAL / UNKNOWN"
    assert result.datasets[0].anomaly_flags == 0


def test_varying_file_count_and_order(tmp_path):
    water = tmp_path / "a.csv"
    energy = tmp_path / "b.csv"
    water_rows = [{"ph": 7 + i / 1000, "conductivity": 500 + i} for i in range(25)]
    energy_rows = [{"energy_kwh": 100 + i, "efficiency": 80 + i / 10, "demand": 90 + i} for i in range(25)]
    _write_csv(water, list(water_rows[0]), water_rows)
    _write_csv(energy, list(energy_rows[0]), energy_rows)
    result = analyze_package([energy, water])
    assert len(result.datasets) == 2
    assert {item.domain for item in result.datasets} == {"ENERGY / RESOURCE", "WATER QUALITY"}
