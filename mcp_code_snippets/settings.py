from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from fastmcp.utilities.mcp_config import MCPConfig

from mcp_code_snippets.explore.detect_language import ProgrammingLanguage


def get_default_mcp_config() -> MCPConfig:
    """Get the default MCP configuration."""
    return MCPConfig(
        mcpServers={
            "mcp-server-qdrant": {
                "url": "https://mcp.qdrant.tech/mcp/",
                "transport": "streamable-http",
            }
        }
    )


class ProxySettings(BaseSettings):
    """Settings for the Qdrant FastMCP Proxy."""

    project_root_path: str = Field(
        default="./",
        validation_alias="PROJECT_ROOT_PATH",
        description="The root path of the project. If not provided, the current working directory will be used.",
    )

    language: Optional[ProgrammingLanguage] = Field(
        default=None,
        validation_alias="PROGRAMMING_LANGUAGE",
        description="The programming language of the project. If not provided, the language will be detected automatically.",
    )

    mcp_proxy_config_path: Optional[str] = Field(
        default=None,
        description="Configuration file with information about remote MCP servers to connect to",
        validation_alias="MCP_PROXY_CONFIG",
    )
