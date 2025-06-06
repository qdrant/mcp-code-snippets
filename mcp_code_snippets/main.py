from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
)
from fastmcp.client import Client
from mcp_code_snippets.config import read_mcp_config
from mcp_code_snippets.proxy import QdrantFastMCPProxy
from mcp_code_snippets.settings import ProxySettings


proxy_settings = ProxySettings()
remote_server_config = read_mcp_config(proxy_settings.mcp_proxy_config_path)
client = Client(remote_server_config)
mcp = QdrantFastMCPProxy(client, proxy_settings=proxy_settings, on_duplicate_tools="replace")


@mcp.tool(name="qdrant-find")
async def qdrant_find(
    query: str, language: str
) -> list[TextContent | ImageContent | EmbeddedResource]:
    arguments = {
        "query": query,
        "language": language,
        "package_name": list(mcp.project_dependencies.keys()),
    }
    async with mcp.client:
        result = await mcp.client.call_tool(
            "qdrant-find",
            arguments=arguments,
        )
        return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
