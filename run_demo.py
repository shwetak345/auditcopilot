from agents.a2a_minimal import Bus
from agents.evidence_agent import EvidenceAgent, AGENT_NAME as EVIDENCE
from agents.audit_agent import AuditAgent, AGENT_NAME as AUDIT

if __name__ == "__main__":
    bus = Bus()
    audit_agent = AuditAgent(bus)
    bus.register(AUDIT, audit_agent.handle)

    evidence_agent = EvidenceAgent(bus)
    result = evidence_agent.start(recipient=AUDIT)

    print("\nResult:", result)
    print("\nOpen the generated report at ./reports/audit_report.md")
