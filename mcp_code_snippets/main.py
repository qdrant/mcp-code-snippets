from typing import Annotated
from pydantic import Field
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
)

from mcp_code_snippets.config import read_mcp_config
from mcp_code_snippets.explore.detect_language import detect_language
from mcp_code_snippets.explore.extract_deps import get_dependencies
from mcp_code_snippets.proxy import QdrantFastMCPProxy
from mcp_code_snippets.settings import ProxySettings


proxy_settings = ProxySettings()
remote_server_config = read_mcp_config(proxy_settings.mcp_proxy_config_path)

mcp = QdrantFastMCPProxy(
    proxy_settings=proxy_settings, remote_server_config=remote_server_config
)


LOOKUP_TOOL_DESCRIPTION = """
Search for examples of using libraries, functions, classes, etc.
Lookup available methods, features and possible configurations.

Example: Create a collection for hybrid search with qdrant client.
"""


@mcp.tool(
    name="lookup-snippet",
    description=LOOKUP_TOOL_DESCRIPTION,
)
async def lookup_snippet(
    query: Annotated[
        str,
        Field(
            description="Description of the function or method to lookup a snippet for."
        ),
    ],
) -> list[TextContent | ImageContent | EmbeddedResource]:
    # Detect parameter values for the remote MCP tool here
    language = proxy_settings.language or detect_language(
        proxy_settings.project_root_path
    )
    packages = get_dependencies(language, proxy_settings.project_root_path)

    # Auto-fill some arguments for the remote MCP tool here
    arguments = {
        "query": query,
        "language": language.value,
        "package_name": list(packages.keys()),
    }
    # Call the remote MCP tool
    async with mcp.client:
        result = await mcp.client.call_tool(
            "qdrant-find",
            arguments=arguments,
        )

        # If empty, try again without filters
        if len(result) == 0:
            result = await mcp.client.call_tool(
                "qdrant-find",
                arguments={"query": query},
            )

        return result


if __name__ == "__main__":
    from mcp_code_snippets.utils import watch_parent

    watch_parent()  # server might not die without explicit kill when the parent process dies (e.g. on closing Cursor)

    mcp.run(transport="stdio")
