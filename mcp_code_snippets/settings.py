from pydantic import Field
from pydantic_settings import BaseSettings


class ProxySettings(BaseSettings):
    """Settings for the Qdrant FastMCP Proxy."""

    pyproject_path: str = Field(default="pyproject.toml", validation_alias="PYPROJECT_PATH")
    mcp_proxy_config_path: str = Field(
        default="mcp_proxy.json",
        description="Configuration file with information about remote MCP servers to connect to",
        validation_alias="MCP_PROXY_CONFIG",
    )
