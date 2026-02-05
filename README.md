# notion-sdk

Python SDK for the Notion API. Thin wrapper with 1:1 endpoint mapping, proven with pytest integration tests.

## Why

The official Notion MCP integration silently drops `properties` on database creation/update. This SDK correctly uses `initial_data_source.properties` and is validated against the live API.

## Install

```bash
pip install -e .
```

## Usage

```python
from notion_sdk import NotionClient

client = NotionClient(api_key="secret_...")

# Create a database with properties that actually work
db = client.create_database(
    parent={"type": "page_id", "page_id": "..."},
    title=[{"text": {"content": "My DB"}}],
    initial_data_source={
        "properties": {
            "Name": {"type": "title", "title": {}},
            "Status": {"type": "select", "select": {
                "options": [{"name": "Done", "color": "green"}]
            }}
        }
    }
)
```

## API Coverage

- **Search**: search
- **Pages**: create, get, update, archive
- **Databases**: create (with properties!), get, update, query
- **Blocks**: get, get children, append children, update, delete
- **Users**: list, get self
- **Comments**: create, list

## Testing

```bash
# Set your Notion API key
export NOTION_API_KEY=secret_...

# Run integration tests
pytest tests/ -v
```
