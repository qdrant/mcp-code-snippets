# MCP Code Snippets

This is an local adapter for MCP server that allows Agents to lookup code snippets in your project.
Local MCP implementation allows to auto-fill some arguments for the remote MCP server, and therefore make lookup more accurate. If no results are found with these arguments, results without arguments are returned.
By default, it uses Qdrant-maintaned remote MCP server with a collection of code snippets, but you can use your own collection by providing a custom MCP proxy configuration.

## Setup

`mcp-code-snippets` should be available as an executable in your system, so that MCP client (like Cursor) can find it.

### Global installation

Simplest option is to install it globally with `pip`:

```bash
pip install mcp-code-snippets
```

In this way it will be available in your system path, and can be used by any MCP client.


### Project installation

Install `mcp-code-snippets` with a package manager of your choice in your project.

An example using `uv`:

```bash
uv add mcp-code-snippets
```

> Note: it might be worth it to install `mcp-code-snippets` as a dev dependency, as it is not needed in production.

### Usage

To start using `mcp-code-snippets` in your project, you need to configure MCP client to use it.

#### Cursor

Add the following to your `.cursor/mcp.json` file:

```json
{
    "mcpServers": {
        "mcp-code-snippets": {
            "command": "mcp-code-snippets"
        }
    }
}
```

### Advanced configuration

`mcp-code-snippest` has one cli argument: --transport, which can be set either to `stdio`, `sse` or `streamable-http`. 
The default is `stdio`.
There is not much other configuration available at the moment, though more to be added.

Other than cli arguments, there are a couple of environment variables to configure the tool:
`PROJECT_ROOT_PATH` and `MCP_PROXY_CONFIG`.

`PROJECT_ROOT_PATH` is the path to the project root. It is used to detect the programming language of the project, and to extract dependencies.
There is an automatic detection of the project language, but you can also specify it manually by setting `PROGRAMMING_LANGUAGE` environment variable.

For Python supported package managers are those following [PyPA specification](https://packaging.python.org/en/latest/specifications/), `poetry` and `uv` syntax beyond PyPA is also supported. 

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
                "MCP_PROXY_CONFIG": "/home/user/my-mcp/mcp_proxy_example.json",
                "PROJECT_ROOT_PATH": "/home/user/my-project"
            }
        }
    }
}
```

`MCP_PROXY_CONFIG` default value is `mcp_proxy.json`, and `PROJECT_ROOT_PATH` defaults to the current directory.

> NOTE: Cursor might not connect to the MCP server with an error like ENOENT mcp-code-snippets, in this case you might need to use absolute paths for all envs and commands.

### Development

This project uses `uv` for package management and `ruff` for linting and formatting.
In order to build the package just run:

```bash
uv build
```

After building, try running the package with:

```bash
mcp-code-snippets --help
```
