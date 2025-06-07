from fastmcp import FastMCP
from fastmcp.utilities.mcp_config import MCPConfig
from fastmcp.client import Client
from fastmcp.server.proxy import FastMCPProxy
from mcp import Tool

from mcp_code_snippets.settings import ProxySettings


class QdrantFastMCPProxy(FastMCPProxy):
    """
    Custom FastMCPProxy to handle Qdrant-specific tools.
    This class can be extended to add more Qdrant-specific functionality if needed.
    """

    def __init__(
        self, proxy_settings: ProxySettings, remote_server_config: MCPConfig, **kwargs
    ):
        self._remote_server_config = remote_server_config
        self._proxy_settings = proxy_settings

        client = Client(remote_server_config)
        super().__init__(client, **kwargs)

    async def get_tools(self) -> dict[str, Tool]:
        # Local tools only
        local_tools = await FastMCP.get_tools(self)
        return local_tools
