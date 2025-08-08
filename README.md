# BlockDAG Message Propagation Monitor 🌐

A lightweight Python tool for visualizing information flow in BlockDAG networks. This tool parses message logs to reveal how blocks and gossip propagate between nodes, helping you understand network dynamics at a glance.

## ✨ Features

- **Message Parsing**: Extracts BLOCK and GOSSIP messages from log files
- **Relationship Tracking**: 
  - Maps parent-child relationships between blocks
  - Links gossips to their referenced blocks
- **Visualization**: 
  - Clean tree-view display of block hierarchy
  - Interactive block exploration
- **Query System**: Get full details for any block on demand

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blockdag-monitor.git
   cd blockdag-monitor