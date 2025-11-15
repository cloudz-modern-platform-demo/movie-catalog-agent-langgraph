# Install Langgraph cli
```
pip install -U "langgraph-cli[inmem]"
```

# Install dependencies
```
uv sync

uv pip install -e .
```

# Setup LLM API Key
```
cp .env.example .env
```

# Run langgraph agent
```
langgraph dev --port 8201
```
