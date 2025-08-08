# display.py
import re
from typing import Dict, Set, Optional
from .models import Block, Gossip
from .storage import MessageStore

def print_summary(store: MessageStore):
    """Print the hierarchical block structure with associated gossips."""
    printed_blocks: Set[str] = set()
    
    # First, print all genesis blocks (blocks without parents)
    for genesis_block in store.get_genesis_blocks():
        _print_block_tree(store, genesis_block.id, printed_blocks, indent=0)
    
    # Then print any remaining blocks (covers orphaned ones)
    for block_id in store.blocks:
        if block_id not in printed_blocks:
            _print_block_tree(store, block_id, printed_blocks, indent=0)

def _print_block_tree(store: MessageStore, block_id: str, printed_blocks: Set[str], indent: int):
    # Skip if block already printed or not found
    if block_id in printed_blocks or block_id not in store.blocks:
        return
    
    printed_blocks.add(block_id)
    block = store.blocks[block_id]
    
    # Print block info with indentation
    prefix = "  " * indent
    parent_str = f"(parents: {', '.join(block.parents)})" if block.parents else "(no parents)"
    print(f"{prefix}BLOCK: {block.id} from {block.from_node} {parent_str}")
    
    # Print transaction details if payload contains them
    tx_info = _extract_transaction_info(block.payload)
    if tx_info:
        print(f"{prefix}  Transaction: {tx_info['from']} → {tx_info['to']} : {tx_info['amount']}")
    
    # Print gossip messages related to this block
    for gossip in store.get_block_gossips(block_id):
        print(f"{prefix}  - GOSSIP: {gossip.from_node} heard about {gossip.heard_about}")
    
    # Recursively print all children of this block
    for child in store.get_block_children(block_id):
        _print_block_tree(store, child.id, printed_blocks, indent + 1)

def _extract_transaction_info(payload: str) -> Optional[Dict]:
    """Extract transaction details from payload if available."""
    patterns = [
        r"tx\s*\{\s*from:\s*(?P<from>\w+),\s*to:\s*(?P<to>\w+),\s*amount:\s*(?P<amount>\d+)",
        r"mint tx\s*\{\s*from:\s*(?P<from>\w+),\s*to:\s*(?P<to>\w+),\s*amount:\s*(?P<amount>\d+)"
    ]
    
    # Try each pattern until one matches
    for pattern in patterns:
        match = re.search(pattern, payload)
        if match:
            return {
                'from': match.group('from'),
                'to': match.group('to'),
                'amount': match.group('amount')
            }
    return None
