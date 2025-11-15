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


# Run a2a remote server
```
uv run movie-catalog-remote-agent
```