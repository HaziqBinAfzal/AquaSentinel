from __future__ import annotations

import io

from aquasentinel.webapp import create_app


def test_web_health() -> None:
    app = create_app()
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["mode"] == "local-read-only"


def test_web_analyzes_uploaded_csv() -> None:
    app = create_app()
    client = app.test_client()
    csv_data = (
        b"timestamp,ph,turbidity,flow\n"
        b"2026-09-01T00:00:00Z,7.1,0.2,100\n"
        b"2026-09-01T00:01:00Z,7.2,0.3,102\n"
        b"2026-09-01T00:02:00Z,7.0,0.2,99\n"
        b"2026-09-01T00:03:00Z,7.1,0.2,101\n"
        b"2026-09-01T00:04:00Z,7.3,0.4,103\n"
    )
    response = client.post(
        "/api/analyze",
        data={"files": (io.BytesIO(csv_data), "evidence.csv")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["evidence_files"] == 1
    assert payload["total_rows"] == 5
    assert payload["datasets"][0]["domain"] == "WATER QUALITY"
    assert payload["datasets"][0]["sha256"]
    assert "authorize industrial-control action" in payload["safety"]


def test_web_rejects_unsupported_extension() -> None:
    app = create_app()
    client = app.test_client()
    response = client.post(
        "/api/analyze",
        data={"files": (io.BytesIO(b"hello"), "evidence.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.get_json()["error"]
