# chepy-mcp

MCP Service for Chepy Library Functions

## Overview

This project exposes the powerful [Chepy](https://github.com/securisec/chepy) data transformation library as an [MCP (Model Context Protocol)](https://gofastmcp.com/getting-started/welcome) server. It allows you to access Chepy's tools (like encoding, decoding, and data manipulation) via a flexible API, including a `bake` pipeline tool inspired by [CyberChef](https://gchq.github.io/CyberChef/).

## Features

- **MCP server** exposing Chepy functions as tools
- **Pipeline tool (`bake`)**: Chain multiple Chepy operations, each with parameters, in a single request
- **Resource endpoint**: Discover all available Chepy operations and their signatures
- **Unittest-based test suite** for robust validation

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/chepy-mcp.git
   cd chepy-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or, if using `pyproject.toml`:
   ```bash
   pip install .
   ```

## Usage

### Start the MCP Server

```bash
python server/main.py
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
python -m unittest discover tests
```

## Extending

- Add new Chepy tools or pipelines by editing `server/main.py`.
- Add more tests in the `tests/` directory.

## Notes

- The `bake` tool will automatically detect if the output is text or binary and encode binary as base64.
- For a list of valid operations and their parameters, see the `resource://chepy_operations` resource.

## License

MIT

---

**Happy hacking with Chepy and MCP!**
