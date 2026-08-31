FRAMEWORKS = {
    "NIST SP 800-82": [
        "Segmented Enterprise/DMZ/OT representation",
        "Controlled administrative-access concept",
        "Passive monitoring and process-aware incident response",
        "Audit/change evidence",
    ],
    "EPA context": [
        "Traceable synthetic water-quality observations",
        "Contamination-event escalation workflow",
        "Public-health-first incident reporting evidence",
    ],
    "WHO water-safety context": [
        "Risk-based quality monitoring",
        "Cross-sensor verification before conclusions",
        "Quality guardrails remain authoritative over optimization",
    ],
}


def report() -> str:
    lines = ["AQUASENTINEL COMPLIANCE / ASSURANCE MAP", "=" * 44]
    for name, evidence in FRAMEWORKS.items():
        lines.append(f"\n{name}")
        lines.extend(f"  - {item}" for item in evidence)
    lines.append("\nEducational mapping only; not a certification or regulatory determination.")
    return "\n".join(lines)
