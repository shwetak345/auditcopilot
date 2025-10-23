from dataclasses import dataclass
import uuid
from typing import Any, Dict

@dataclass
class A2AEnvelope:
    sender: str
    recipient: str
    kind: str
    payload: Dict[str, Any]
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

class Bus:
    def __init__(self):
        self.handlers = {}

    def register(self, name, handler):
        self.handlers[name] = handler

    def send(self, env: A2AEnvelope):
        h = self.handlers.get(env.recipient)
        if not h:
            raise RuntimeError(f'No handler for {env.recipient}')
        return h(env)
