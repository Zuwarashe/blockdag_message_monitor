# parser.py
import re
from datetime import datetime
from typing import Optional, List, Union
from .models import Block, Gossip

def extract_field(raw_message: str, field_name: str) -> str:
    """Get the value of a specific field from the message."""
    lines = raw_message.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
    # Different possible formats to match
    prefixes = [
        f"# {field_name}:",
        f"#{field_name}:",
        f"{field_name}:"
    ]
    
    # Look for the matching field
    for line in lines:
        line = line.strip()
        for prefix in prefixes:
            if line.startswith(prefix):
                return line[len(prefix):].strip()
    
    # If not found, print debug info and raise error
    print(f"\nDEBUG: Field '{field_name}' not found")
    print("Searching in message:")
    print(repr(raw_message))
    print("All lines:")
    for i, line in enumerate(lines):
        print(f"{i}: {repr(line)}")
    raise ValueError(f"Required field '{field_name}' not found")

def parse_timestamp(timestamp_str: str) -> datetime:
    """Convert timestamp string into datetime object."""
    return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")

def parse_parents(parents_str: str) -> List[str]:
    """Turn parents string into a list."""
    if not parents_str or parents_str == "[]":
        return []
    return [p.strip() for p in parents_str[1:-1].split(",")]

def extract_payload(raw_message: str) -> str:
    """Get the payload text from the message."""
    payload_match = re.search(r'PAYLOAD:\s*(.*?)(?=\s*---|\s*$)', raw_message, re.DOTALL)
    return payload_match.group(1).strip() if payload_match else ""

def extract_heard_about(payload: str) -> Optional[str]:
    """Find the block ID mentioned in a gossip payload."""
    match = re.search(r"heard about (BDG-\d+)", payload)
    return match.group(1) if match else None

def parse_message(raw_message: str, message_id: str) -> Union[Block, Gossip]:
    """Convert a raw message string into a Block or Gossip object."""
    from_node = extract_field(raw_message, "FROM")
    msg_type = extract_field(raw_message, "TYPE")
    timestamp = parse_timestamp(extract_field(raw_message, "TIMESTAMP"))
    payload = extract_payload(raw_message)

    # If it's a block, parse parents too
    if msg_type == "BLOCK":
        parents_str = extract_field(raw_message, "PARENTS")
        parents = parse_parents(parents_str)
        return Block(
            id=message_id,
            from_node=from_node,
            type=msg_type,
            timestamp=timestamp,
            payload=payload,
            parents=parents
        )
    else:
        # Otherwise, it's a gossip message
        heard_about = extract_heard_about(payload)
        return Gossip(
            id=message_id,
            from_node=from_node,
            type=msg_type,
            timestamp=timestamp,
            payload=payload,
            heard_about=heard_about
        )

def parse_messages(raw_log: str) -> List[Union[Block, Gossip]]:
    """Split the log into messages and parse them all."""
    # Normalize newlines
    normalized_log = raw_log.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split messages by separator
    raw_messages = [msg.strip() for msg in normalized_log.split('---\n') if msg.strip()]
    
    if not raw_messages:
        raise ValueError("No valid messages found. Check your message separators ('---')")
    
    # Debug: show found messages
    print(f"Found {len(raw_messages)} messages to parse")
    for i, msg in enumerate(raw_messages, 1):
        print(f"\nMessage {i} content:")
        print(repr(msg))
        
    # Parse each message into an object
    return [parse_message(msg, f"BDG-{i+1:03d}") for i, msg in enumerate(raw_messages)]
