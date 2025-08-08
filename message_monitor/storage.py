# storage.py
from typing import Dict, List
from .models import Block, Gossip

class MessageStore:
    def __init__(self):
        # Store blocks by their ID
        self.blocks: Dict[str, Block] = {}
        
        # Store all gossip messages
        self.gossips: List[Gossip] = []
        
        # Keep track of block relationships and gossips
        self.block_index: Dict[str, Dict] = {}  # {block_id: {'children': [], 'gossips': []}}
    
    def add_message(self, message):
        # Decide if message is a block or gossip and store accordingly
        if message.type == "BLOCK":
            self._add_block(message)
        else:
            self._add_gossip(message)
    
    def _add_block(self, block: Block):
        # Save the block in storage
        self.blocks[block.id] = block
        
        # Create index entry for this block
        self.block_index[block.id] = {
            'children': [],
            'gossips': []
        }
        
        # Link this block to its parents
        for parent_id in block.parents:
            if parent_id in self.block_index:
                self.block_index[parent_id]['children'].append(block.id)
    
    def _add_gossip(self, gossip: Gossip):
        # Save gossip in the list
        self.gossips.append(gossip)
        
        # Link gossip to its block if known
        if gossip.heard_about and gossip.heard_about in self.block_index:
            self.block_index[gossip.heard_about]['gossips'].append(gossip)
    
    def get_genesis_blocks(self) -> List[Block]:
        """Return blocks with no parents."""
        return [block for block in self.blocks.values() if not block.parents]
    
    def get_block_children(self, block_id: str) -> List[Block]:
        """Return all children of a block."""
        return [self.blocks[child_id] for child_id in self.block_index.get(block_id, {}).get('children', [])]
    
    def get_block_gossips(self, block_id: str) -> List[Gossip]:
        """Return all gossips about a block."""
        return self.block_index.get(block_id, {}).get('gossips', [])
