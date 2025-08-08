# cli.py
from message_monitor.display import _extract_transaction_info
from .storage import MessageStore

def interactive_query(store: MessageStore):
    """Allow user to query blocks by ID."""
    print("\nInteractive mode (type 'quit' to exit)")
    while True:
        block_id = input("\nQuery block ID: ").strip()
        
        # Exit if user types "quit"
        if block_id.lower() == 'quit':
            break
            
        # If the block exists in storage
        if block_id in store.blocks:
            block = store.blocks[block_id]
            
            # Show main block details
            print(f"\nDetails for {block_id}:")
            print(f"From: {block.from_node}")
            print(f"Type: {block.type}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Parents: {', '.join(block.parents) if block.parents else 'None'}")
            print(f"Payload: {block.payload}")
            
            # Show transaction details if payload contains them
            tx_info = _extract_transaction_info(block.payload)
            if tx_info:
                print(f"\nTransaction Details:")
                print(f"From: {tx_info['from']}")
                print(f"To: {tx_info['to']}")
                print(f"Amount: {tx_info['amount']}")
            
            # Show related gossips for this block
            gossips = store.get_block_gossips(block_id)
            if gossips:
                print("\nAssociated Gossips:")
                for gossip in gossips:
                    print(f"- {gossip.from_node} at {gossip.timestamp}")
        else:
            # If block is not found
            print(f"Block {block_id} not found.")
