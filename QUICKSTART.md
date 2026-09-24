# Quick Start Guide

## Prerequisites Check

Before running the experiments, ensure you have:

1. **Python 3.10+** installed
   ```bash
   python --version
   ```

2. **OpenAI API Key** - Get one at https://platform.openai.com/api-keys

## Setup (5 minutes)

### Step 1: Install Dependencies

```bash
# Install required packages
pip install mcp openai python-dotenv
```

### Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your actual key
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

**Important:** Never commit your `.env` file to git!

## Running Experiments

### Experiment 1: Personal Assistant (Memory)

```bash
cd experiment-1-personal-assistant
python client.py
```

**Try these commands:**
- "Remember that my project deadline is October 1"
- "What did I say about the project?"
- "Remember I have a dentist appointment on October 15"
- "When is my dentist appointment?"

### Experiment 2: Weather Dashboard

```bash
cd experiment-2-data-dashboard
python client.py
```

**Try these commands:**
- "What's the weather in Tokyo?"
- "How's the weather in Paris?"
- "Tell me about London's weather"

## Testing Without OpenAI

If you don't have an OpenAI API key yet, you can still test the MCP servers:

```bash
# Test Experiment 1 server
python test_experiment1.py

# Test Experiment 2 server
python test_experiment2.py
```

## Troubleshooting

### "No module named 'mcp'"
```bash
pip install mcp
```

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in the project root (not inside experiment folders)
- Verify the key starts with `sk-`
- Make sure `python-dotenv` is installed

### Import errors
```bash
# Reinstall all dependencies
pip install --upgrade mcp openai python-dotenv
```

## Next Steps

1. Read the main [README.md](README.md) for detailed explanations
2. Explore each experiment's README:
   - [Experiment 1 README](experiment-1-personal-assistant/README.md)
   - [Experiment 2 README](experiment-2-data-dashboard/README.md)
3. Modify the code to add new features
4. Try building your own MCP server!

## Common Commands

```bash
# View saved notes
cat experiment-1-personal-assistant/notes.json

# Clear notes
echo "[]" > experiment-1-personal-assistant/notes.json

# Exit client
Type: quit or exit
```

Happy experimenting! 🚀
