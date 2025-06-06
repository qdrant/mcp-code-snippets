from enum import Enum

import typer


class Transport(str, Enum):
    stdio = "stdio"
    sse = "sse"
    streamable_http = "streamable-http"


app = typer.Typer(name="MCP Code snippets", help="CLI for MCP code snippest")


@app.command(name="run")
def run(transport: Transport = Transport.stdio):
    from mcp_code_snippets.main import mcp

    mcp.run(transport=transport)


if __name__ == "__main__":
    app()
