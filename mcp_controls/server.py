import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "systems.json"

class MCPControlsServer:
    def __init__(self, data_path: Path = DATA_PATH):
        with open(data_path, "r", encoding="utf-8") as f:
            self._db = json.load(f)

    def get_system_list(self):
        return [{"name": s["name"], "owner": s["owner"], "env": s["env"]} for s in self._db.get("systems", [])]

    def get_control_state(self, name: str):
        for s in self._db.get("systems", []):
            if s["name"].lower() == name.lower():
                return {"name": s["name"], "controls": s["controls"]}
        raise KeyError(name)

    def get_audit_log(self, name: str):
        return {"name": name, "events": [{"ts": "2025-10-21T09:00:00Z", "msg": "deployment rolled out"}]}

SERVER = MCPControlsServer()
