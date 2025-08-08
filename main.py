# main.py
import sys
from message_monitor.parser import parse_messages
from message_monitor.storage import MessageStore
from message_monitor.display import print_summary
from message_monitor.cli import interactive_query

def main():
    # Make sure a file name is given
    if len(sys.argv) < 2:
        print("Usage: python main.py <logfile.txt>")
        print("Example: python main.py blockdag_log.txt")
        return

    filename = sys.argv[1]
    
    try:
        # Open and read the log file
        with open(filename, 'r') as file:
            log_content = file.read()
        
        # Turn log content into message objects
        messages = parse_messages(log_content)
        
        # Store messages in memory
        store = MessageStore()
        for message in messages:
            store.add_message(message)
        
        # Print summary view
        print("\n=== BlockDAG Message Propagation Summary ===")
        print_summary(store)
        
        # Allow user to query details interactively
        interactive_query(store)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
