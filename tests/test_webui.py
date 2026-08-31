from aquasentinel.webui import HTML


def test_web_dashboard_starts_without_demo_data():
    assert "No dataset loaded" in HTML
    assert "Nothing is preloaded" in HTML
    assert "type=\"file\"" in HTML
    assert "/api/analyze" in HTML


def test_web_dashboard_is_local_and_read_only():
    assert "127.0.0.1" in HTML
    assert "No automated industrial control" in HTML
    assert ".log,.txt,.csv,.json,.jsonl" in HTML


def test_web_dashboard_uses_restrained_topic_133_workstation_language():
    assert "Local analysis workstation" in HTML
    assert "Source profile" in HTML
    assert "Water quality assurance" in HTML
    assert "Desalination process & predictive maintenance" in HTML
    assert "OT / SCADA security evidence" in HTML
    assert "AI anomaly detection" in HTML
    assert "Cyber-physical correlation & response evidence" in HTML
    assert "Energy & resource review" in HTML
    assert "Source records — recent evidence" in HTML
