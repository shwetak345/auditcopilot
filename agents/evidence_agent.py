from mcp_controls.server import SERVER
from .a2a_minimal import A2AEnvelope

AGENT_NAME = "EvidenceAgent"

class EvidenceAgent:
    def __init__(self, bus):
        self.bus = bus

    def start(self, recipient: str):
        systems = SERVER.get_system_list()
        evidence = []
        for s in systems:
            name = s["name"]
            controls = SERVER.get_control_state(name)
            logs = SERVER.get_audit_log(name)
            evidence.append({"system": s, "controls": controls["controls"], "logs": logs["events"]})
        env = A2AEnvelope(sender=AGENT_NAME, recipient=recipient, kind="evidence_bundle", payload={"evidence": evidence})
        return self.bus.send(env)
