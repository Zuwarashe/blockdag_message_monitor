# BlockDAG Message Propagation Monitor 🌐

A lightweight Python tool for visualizing information flow in BlockDAG networks.

## ✨ Features
- **Message Parsing**: Extracts `BLOCK` and `GOSSIP` messages
- **Relationship Tracking**:
  - Parent → child block relationships
  - Gossip ↔ block references
- **Visualization**:
  - ASCII tree-view hierarchy
  - Interactive exploration
- **Query System**: Full block details on demand

## 🛠 Installation
```bash
# 1. Clone repository
git clone https://github.com/yourusername/blockdag-monitor.git
cd blockdag-monitor

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

## 🚀 Usage
python main.py your_logfile.txt
