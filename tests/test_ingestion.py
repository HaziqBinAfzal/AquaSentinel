from aquasentinel.ingestion import analyze_content, parse_content


def test_csv_water_data_is_analyzed():
    content = (
        "timestamp,severity,ph,conductivity,turbidity,ro_pressure,flow_rate,membrane_health\n"
        "2026-01-01T00:00:00Z,info,7.2,420,0.3,58,102,92\n"
        "2026-01-01T00:01:00Z,warning,6.1,720,2.8,61,96,68\n"
    )
    result = analyze_content("water.csv", content)
    assert result["source"]["records"] == 2
    assert "ph" in result["metrics"]
    assert result["summary"]["warnings"] == 1
    assert result["review_flags"]


def test_plain_log_extracts_severity_and_indicators():
    content = (
        "2026-01-01T00:00:00Z INFO service started\n"
        "2026-01-01T00:00:03Z WARNING unexpected scada session denied\n"
        "2026-01-01T00:00:05Z ERROR pressure timeout\n"
    )
    result = analyze_content("plant.log", content)
    assert result["severity_counts"]["warning"] == 1
    assert result["severity_counts"]["error"] == 1
    assert result["indicators"]["scada"] == 1
    assert result["indicators"]["pressure"] == 1


def test_jsonl_is_supported():
    dataset = parse_content(
        "events.jsonl",
        '{"timestamp":"2026-01-01T00:00:00Z","level":"info","flow_rate":101}\n'
        '{"timestamp":"2026-01-01T00:01:00Z","level":"warning","flow_rate":92}\n',
    )
    assert dataset.format == "jsonl"
    assert len(dataset.records) == 2


def test_unsupported_file_type_is_rejected():
    try:
        parse_content("data.exe", "abc")
    except ValueError as exc:
        assert "Unsupported file type" in str(exc)
    else:
        raise AssertionError("unsupported file type should fail")
