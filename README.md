### Setup

Install `mcp-code-snippets` with a package manager of your choice in your project.

An example using `uv`:

```bash
uv add mcp-code-snippets
```

> Note: it might be worth it to install `mcp-code-snippets` as a dev dependency, as it is not needed in production.

### Usage

The simplest way to launch is to just run:

```bash
mcp-code-snippets
```

#### Configuration

`mcp-code-snippest` has one cli argument: --transport, which can be set either to `stdio`, `sse` or `streamable-http`. 
The default is `stdio`.
There is not much other configuration available at the moment, though more to be added.

Other than cli arguments, there are a couple of environment variables to configure the tool:
`PYPROJECT_PATH` and `MCP_PROXY_CONFIG`.

`PYPROJECT_PATH` is the path to the `pyproject.toml` file which is used as a filter in requests to the MCP server to make it search only among relevant code snippets.
The supported package managers are those following [PyPA specification](https://packaging.python.org/en/latest/specifications/), `poetry` and `uv` syntax beyond PyPA is also supported. 

`MCP_PROXY_CONFIG` is the path to the MCP proxy configuration file, which is used to configure the access to the MCP server with the code snippets.

An example would be:

```json
{
     "mcpServers": {
         "mcp-server-qdrant": {
             "url": "https://mcp.qdrant.tech/mcp/",
             "transport": "streamable-http"
         }
     }
}
```

#### Editors integrations

You can use `mcp-code-snippets` with various editors that support MCP protocol.
An example configuration for [Cursor](https://www.cursor.com/) in `.cursor/mcp.json` would look like this:

```json
{
    "mcpServers": {
        "mcp-code-snippets": {
            "command": "mcp-code-snippets",
            "env": {
                "MCP_PROXY_CONFIG": "mcp_proxy_example.json",
                "PYPROJECT_PATH": "pyproject.toml"
            }
        }
    }
}
```

`MCP_PROXY_CONFIG` default value is `mcp_proxy.json`, and `PYPROJECT_PATH` defaults to `pyproject.toml` in the current directory.

> NOTE: Cursor might not connect to the MCP server with an error like ENOENT mcp-code-snippets, in this case you might need to use absolute paths for all envs and commands.

### Development

This project uses `uv` for package management and `ruff` for linting and formatting.
In order to build the package just run:

```bash
uv build
```

Try running 