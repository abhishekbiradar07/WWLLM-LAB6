# Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] pip package manager available
- [ ] OpenAI API account with credits
- [ ] Internet connection

## Step-by-Step Setup

### 1. Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### 2. Configure Environment Variables

```bash
# Create .env file in the project root
cp .env.example .env

# Edit .env and paste your API key
# .env should contain:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**IMPORTANT:** Never commit your `.env` file to Git!

### 3. Install Dependencies

Choose one experiment or install both:

**Option A: Install for Experiment 1**
```bash
cd experiment-1-personal-assistant
pip install -r requirements.txt
```

**Option B: Install for Experiment 2**
```bash
cd experiment-2-data-dashboard
pip install -r requirements.txt
```

**Option C: Install both**
```bash
pip install mcp openai python-dotenv
```

### 4. Run the Experiments

**Experiment 1: Personal Assistant**
```bash
cd experiment-1-personal-assistant
python client.py
```

Try these commands:
- "Remember that my project deadline is October 1"
- "What did I say about the deadline?"
- "Remember I have a dentist appointment on Friday at 2pm"
- "When is my dentist appointment?"

**Experiment 2: Weather Dashboard**
```bash
cd experiment-2-data-dashboard
python client.py
```

Try these commands:
- "What's the weather in Tokyo?"
- "How's the weather in Paris?"
- "Tell me about the weather in New York"

### 5. Exit the Programs

Type `quit` or `exit` or press `Ctrl+C`

## Troubleshooting

### "No module named 'mcp'"
```bash
pip install mcp
```

### "OpenAI API key not found" 
- Check that `.env` file exists in project root
- Verify the key is correct and starts with `sk-`
- Make sure you're running from the correct directory

### "Invalid API key"
- Your API key might be incorrect or expired
- Generate a new key at https://platform.openai.com/api-keys
- Update the `.env` file

### "Connection refused" or server errors
- Make sure you're running `client.py`, not `server.py`
- The client automatically starts the server

### Weather API timeout
- Check internet connection
- Try a different city name
- Wait a moment and try again

### Dependency conflicts (warnings during pip install)
- These are usually safe to ignore if the installation succeeds
- The experiments use minimal dependencies and should work despite warnings

## Cost Considerations

Both experiments use OpenAI's GPT-4o-mini model, which is very affordable:
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens

Typical usage:
- Each interaction: ~500-1000 tokens
- Cost per interaction: Less than $0.001 (fraction of a cent)
- 100 interactions: Less than $0.10

## Testing Without Full Client

You can test the MCP servers independently without OpenAI:

**Test Experiment 1 Server:**
```python
# Create test_server1.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}")

asyncio.run(test())
```

Run: `python test_server1.py`

## Next Steps

Once everything works:
1. Read the main README.md for architecture details
2. Explore the code in `server.py` and `client.py`
3. Try modifying the tools or adding new features
4. Experiment with different prompts and queries
5. Check out the MCP documentation: https://modelcontextprotocol.io/

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Review the experiment-specific README files
3. Verify all prerequisites are met
4. Check Python and pip versions
5. Ensure `.env` file is properly configured

Happy experimenting! 🚀
