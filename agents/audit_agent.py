from pathlib import Path
from rich.console import Console
from rich.table import Table

AGENT_NAME = "AuditAgent"
REPORT_PATH = Path("reports/audit_report.md")

RISK_RULES = [
    ("tls_enabled", False, "TLS disabled", "Enable TLS 1.2+ for all endpoints"),
    ("auth_required", False, "No authentication on APIs", "Enforce auth (OAuth2/JWT)"),
    ("encryption_at_rest", False, "No encryption at rest", "Enable storage encryption"),
    ("backups_enabled", False, "Backups disabled", "Set up automated backups + DR test"),
]

SEVERITY = {
    "TLS disabled": "High",
    "No authentication on APIs": "Critical",
    "No encryption at rest": "High",
    "Backups disabled": "Medium",
}

class AuditAgent:
    def __init__(self, bus):
        self.bus = bus

    def handle(self, env):
        if env.kind != "evidence_bundle":
            return {"status": "ignored"}
        evidence = env.payload["evidence"]
        findings = []
        for item in evidence:
            sys = item["system"]
            controls = item["controls"]
            sys_findings = []
            for key, bad, msg, rec in RISK_RULES:
                if controls.get(key) is bad:
                    sys_findings.append({"issue": msg, "recommendation": rec, "severity": SEVERITY[msg]})
            findings.append({"system": sys["name"], "env": sys["env"], "owner": sys["owner"], "findings": sys_findings})
        self._write_report(findings)
        self._print_summary(findings)
        return {"status": "ok", "report": str(REPORT_PATH)}

    def _write_report(self, findings):
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# Audit Summary\n"]
        for f in findings:
            lines.append(f"\n## System: {f['system']} ({f['env']}) — Owner: {f['owner']}\n")
            if not f["findings"]:
                lines.append("All baseline controls present.\n")
            else:
                for g in f["findings"]:
                    lines.append(f"- **{g['severity']}** — {g['issue']}\n  - Recommendation: {g['recommendation']}\n")
        REPORT_PATH.write_text("".join(lines), encoding="utf-8")

    def _print_summary(self, findings):
        console = Console()
        table = Table(title="AuditCopilot Summary")
        table.add_column("System")
        table.add_column("Env")
        table.add_column("Owner")
        table.add_column("Issues")
        for f in findings:
            issues = ", ".join(g["issue"] for g in f["findings"]) or "None"
            table.add_row(f["system"], f["env"], f["owner"], issues)
        console.print(table)
