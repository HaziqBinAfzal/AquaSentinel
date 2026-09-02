"""Local browser workstation for AquaSentinel evidence analysis.

The web UI is intentionally localhost-only by default. Uploaded evidence is written to a
temporary directory for the duration of the request, analyzed by the same schema-driven
engine used by the terminal workflow, and then removed.
"""
from __future__ import annotations

import argparse
import tempfile
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from .evidence import SUPPORTED_SUFFIXES, analyze_package

MAX_UPLOAD_BYTES = 64 * 1024 * 1024


def _dataset_payload(dataset) -> dict[str, object]:
    return {
        "name": dataset.name,
        "file_type": dataset.file_type,
        "rows": dataset.rows,
        "columns": dataset.columns,
        "domain": dataset.domain,
        "confidence": round(dataset.confidence * 100.0, 1),
        "numeric_features": dataset.numeric_features,
        "missing_pct": round(dataset.missing_pct, 2),
        "anomaly_score": dataset.anomaly_score,
        "anomaly_flags": dataset.anomaly_flags,
        "analyzed_rows": dataset.analyzed_rows,
        "analysis_method": dataset.analysis_method,
        "timestamp_field": dataset.timestamp_field,
        "time_start": dataset.time_start,
        "time_end": dataset.time_end,
        "sha256": dataset.sha256,
        "notes": dataset.notes,
    }


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

    @app.get("/")
    def index():
        return render_template("workstation.html")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "mode": "local-read-only"})

    @app.post("/api/analyze")
    def analyze():
        uploads = request.files.getlist("files")
        uploads = [item for item in uploads if item and item.filename]
        if not uploads:
            return jsonify({"error": "Select at least one evidence file."}), 400

        with tempfile.TemporaryDirectory(prefix="aquasentinel-web-") as folder:
            paths: list[Path] = []
            used: set[str] = set()
            for index, upload in enumerate(uploads, start=1):
                original = Path(upload.filename).name
                suffix = Path(original).suffix.lower()
                if suffix not in SUPPORTED_SUFFIXES:
                    return jsonify(
                        {"error": f"Unsupported file type for {original}: {suffix or 'none'}"}
                    ), 400
                filename = secure_filename(original) or f"evidence-{index}{suffix}"
                candidate = filename
                counter = 1
                while candidate.lower() in used:
                    candidate = f"{Path(filename).stem}-{counter}{suffix}"
                    counter += 1
                used.add(candidate.lower())
                destination = Path(folder) / candidate
                upload.save(destination)
                paths.append(destination)

            try:
                package = analyze_package(paths)
            except (ValueError, OSError) as exc:
                return jsonify({"error": f"Evidence analysis failed: {exc}"}), 400

            return jsonify(
                {
                    "risk_score": package.risk_score,
                    "risk_level": package.risk_level,
                    "total_rows": package.total_rows,
                    "total_flags": package.total_flags,
                    "evidence_files": len(package.datasets),
                    "correlations": package.correlations,
                    "datasets": [_dataset_payload(item) for item in package.datasets],
                    "safety": (
                        "Advisory evidence analysis only. Results do not certify water safety, "
                        "confirm compromise, or authorize industrial-control action."
                    ),
                }
            )

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "Upload is too large. Maximum request size is 64 MB."}), 413

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="AquaSentinel local browser workstation")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    if not args.no_browser:
        webbrowser.open(f"http://{args.host}:{args.port}")
    create_app().run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
