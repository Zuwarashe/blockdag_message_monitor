# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# Base message structure
@dataclass
class Message:
    id: str
    from_node: str
    type: str
    timestamp: datetime
    payload: str

# Block message with parent references
@dataclass
class Block(Message):
    parents: List[str]

# Gossip message with optional "heard about" reference
@dataclass
class Gossip(Message):
    heard_about: Optional[str] = None
