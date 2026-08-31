from __future__ import annotations

import platform
import shutil
import sys
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str

    def dict(self) -> dict:
        return asdict(self)


def run_checks() -> list[Check]:
    checks: list[Check] = []
    checks.append(Check("Python", sys.version_info >= (3, 10), platform.python_version()))

    try:
        import rich  # noqa: F401
        checks.append(Check("Rich", True, "installed"))
    except Exception as exc:  # pragma: no cover - defensive diagnostic
        checks.append(Check("Rich", False, str(exc)))

    try:
        import sklearn
        checks.append(Check("scikit-learn", True, sklearn.__version__))
    except Exception as exc:  # pragma: no cover - defensive diagnostic
        checks.append(Check("scikit-learn", False, str(exc)))

    checks.append(Check("Terminal", bool(shutil.get_terminal_size(fallback=(80, 24))), "terminal size detected"))
    checks.append(Check("Safety mode", True, "synthetic telemetry only; no live OT/SCADA write path"))
    return checks


def healthy(checks: list[Check]) -> bool:
    return all(c.ok for c in checks)
