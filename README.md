# chepy-mcp

MCP Service for Chepy Library Functions

## Overview

This project exposes the powerful [Chepy](https://github.com/securisec/chepy) data transformation library as an [MCP (Model Context Protocol)](https://gofastmcp.com/getting-started/welcome) server. It allows you to access Chepy's tools (like encoding, decoding, and data manipulation) via a single flexible API: the `bake` pipeline tool, inspired by [CyberChef](https://gchq.github.io/CyberChef/).

## Features

- **Single pipeline tool (`bake`)**: Chain one or more Chepy operations, each with parameters, in a single request
- **Resource endpoint**: Discover all available Chepy operations and their signatures
- **Unittest-based test suite** for robust validation

## Installation
1. **Install uv if it is not installed yet.**
    ```bash
    $ curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/nebucaz/chepy-mcp.git
   cd chepy-mcp
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

## Run

Run the server with:
```bash
$ uv run src/server.py
```

### Start the MCP Server

You can run the server directly:
```bash
uv python server/main.py
```

Or, using the [mcp CLI](https://gofastmcp.com/getting-started/welcome):
```bash
uv run mcp
```

### Example: Using the `bake` Tool

Send a request to the `bake` tool with a pipeline of operations:

```json
{
  "input": "hello world",
  "pipeline": [
    {"op": "to_base64"},
    {"op": "from_base64"}
  ]
}
```

The response will indicate if the output is text or binary:
```json
{
  "type": "text",
  "data": "hello world"
}
```

### Discover Available Operations

Fetch the resource endpoint to get all available Chepy operations and their parameter signatures:

- **Resource URI:** `resource://chepy_operations`

Example response:
```json
{
  "to_base64": "(self, alphabet: str = 'standard') -> ~DataFormatT",
  "from_base64": "(self, alphabet: str = 'standard', remove_non_alpha: bool = True) -> ~DataFormatT",
  ...
}
```

## Testing

Run the test suite with:

```bash
uv python -m unittest discover tests
```

## Extending

- All Chepy operations are available through the pipeline tool; no need to add individual wrappers.
- Add more tests in the `tests/` directory as needed.

## Notes

- The `bake` tool will automatically detect if the output is text or binary and encode binary as base64.
- For a list of valid operations and their parameters, see the `resource://chepy_operations` resource.
- Only the `bake` tool and the Chepy operations resource are exposed for maximum flexibility and maintainability.

## License

MIT

---

**Happy hacking with Chepy and MCP!**
