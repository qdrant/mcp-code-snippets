import sys
from typing import Any

from fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import (
    METHOD_NOT_FOUND,

)
from fastmcp.client import Client
from fastmcp.tools.tool import Tool
from fastmcp.server.proxy import FastMCPProxy, ProxyTool

from mcp_code_snippets.settings import ProxySettings
from mcp_code_snippets.utils import parse_dependencies


def infer_parameter_descriptions(
    local_tool_schema: dict[str, Any], remote_tool_schema: dict[str, Any]
) -> None:
    local_properties = local_tool_schema.get("properties", {})
    remote_properties = remote_tool_schema.get("properties", {})
    local_parameter_names = local_properties.keys()
    remote_parameter_names = remote_properties.keys()
    for name in local_parameter_names:
        if name not in remote_parameter_names:
            continue
        local_property = local_properties[name]
        remote_property = remote_properties[name]
        if "description" not in local_property and "description" in remote_property:
            local_property["description"] = remote_property["description"]


def update_proxy_tool(local_tool: Tool, remote_tool: ProxyTool) -> None:
    """Enrich the locally overridden version of a remote server tool with its metadata if needed.

    Args:
        local_tool: The locally overridden version of the tool.
        remote_tool: The remote server version of the tool.
    """

    if local_tool.description is None:
        local_tool.description = remote_tool.description
    if local_tool.tags is None:
        local_tool.tags = remote_tool.tags
    if local_tool.annotations is None:
        local_tool.annotations = remote_tool.annotations
    infer_parameter_descriptions(local_tool.parameters, remote_tool.parameters)


class QdrantFastMCPProxy(FastMCPProxy):
    """
    Custom FastMCPProxy to handle Qdrant-specific tools.
    This class can be extended to add more Qdrant-specific functionality if needed.
    """

    def __init__(self, client: Client, proxy_settings: ProxySettings, **kwargs):
        super().__init__(client, **kwargs)
        self._proxy_settings = proxy_settings
        self.project_dependencies = parse_dependencies(proxy_settings.pyproject_path)

    async def get_tools(self) -> dict[str, Tool]:
        tools = {}
        async with self.client:
            try:
                client_tools = await self.client.list_tools()
            except McpError as e:
                if e.error.code == METHOD_NOT_FOUND:
                    client_tools = []
                else:
                    raise e
            for tool in client_tools:
                tool_proxy = await ProxyTool.from_client(self.client, tool)
                tools[tool_proxy.name] = tool_proxy

        local_tools = await FastMCP.get_tools(self)

        for tool_name, tool in local_tools.items():
            if tool_name not in tools:
                tools[tool_name] = tool
            else:
                if self._tool_manager.duplicate_behavior == "warn":
                    print(f"Warning: Tool {tool_name} already exists, skipping.", file=sys.stderr)
                elif self._tool_manager.duplicate_behavior == "replace":
                    update_proxy_tool(tool, tools[tool_name])
                    tools[tool_name] = tool
                elif self._tool_manager.duplicate_behavior == "ignore":
                    continue
                else:
                    raise ValueError(
                        f"Unknown on_duplicate_tools behavior: {self._tool_manager.duplicate_behavior}"
                    )

        return tools



