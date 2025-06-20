# chepy-mcp

MCP Service for Chepy Library Functions

## Overview

This project exposes the powerful [Chepy](https://github.com/securisec/chepy) data transformation library as an [MCP (Model Context Protocol)](https://gofastmcp.com/getting-started/welcome) server. It allows you to access Chepy's tools (like encoding, decoding, and data manipulation) via a single flexible API: the `bake` pipeline tool, inspired by [CyberChef](https://gchq.github.io/CyberChef/).

## Features

- **Single pipeline tool (`bake`)**: Chain one or more Chepy operations, each with parameters, in a single request
- **Chepy recipe JSON format**: Pipelines are described using Chepy's own recipe serialization, making them compatible with Chepy's import/export and CLI tools
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

## Usage

### The Chepy Recipe JSON Format

The `bake` tool expects a pipeline in the [Chepy recipe JSON format](https://chepy.readthedocs.io/en/latest/recipes.html):

```json
{
  "input": "hello world",
  "recipe": [
    {"function": "to_base64", "args": {}},
    {"function": "from_base64", "args": {}}
  ]
}
```

- Each step in the `recipe` list is an object with a `function` (the Chepy operation name) and `args` (a dictionary of arguments for that function).
- This format is fully compatible with Chepy's own recipe import/export and CLI tools.

The response will indicate if the output is text or binary:
```json
{
  "type": "text",
  "data": "hello world"
}
```

### Discover Available Operations

Fetch the resource endpoint to get all available Chepy operations, their parameter signatures, and descriptions:

- **Resource URI:** `resource://chepy_operations`

Example response:
```json
{
  "to_base64": {
    "signature": "(alphabet: str = 'standard')",
    "description": "Encode the input string to base64"
  },
  "from_base64": {
    "signature": "(alphabet: str = 'standard', remove_non_alpha: bool = True)",
    "description": "Decode base64 encoded string"
  }
  // ...
}
```

## Extending

- All Chepy operations are available through the pipeline tool; no need to add individual wrappers.
- Add more tests in the `tests/` directory as needed.

## Notes

- The `bake` tool will automatically detect if the output is text or binary and encode binary as base64.
- For a list of valid operations and their parameters, see the `resource://chepy_operations` resource.
- Only the `bake` tool and the Chepy operations resource are exposed for maximum flexibility and maintainability.
- The pipeline format is fully compatible with Chepy's own recipe serialization and CLI tools.

## License

MIT

---

**Happy hacking with Chepy and MCP!**
