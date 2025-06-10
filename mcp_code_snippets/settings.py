import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
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

    @field_validator("project_root_path", mode="before")
    @classmethod
    def validate_project_root_path(cls, v: str) -> str:
        """Validate the project root path

        PROJECT_ROOT_PATH is assumed to be set manually, so it takes precedence over the other cases.
        WORKSPACE_FOLDER_PATHS is an environment variable coming from Cursor. By default, Cursor assumes that
            paths are relative to the system root when it's launching MCP servers. This might be inconvenient, and we
            replace default value './' with the current working directory.

        Args:
            v (str): The project root path from the environment variable or default value.
        """
        project_root_env = os.environ.get("PROJECT_ROOT_PATH")
        workspace_folder_paths_env = os.environ.get("WORKSPACE_FOLDER_PATHS")

        if project_root_env:
            v = project_root_env
        elif workspace_folder_paths_env:
            v = workspace_folder_paths_env

        if v == './':
            abs_path = Path(v).resolve()
            if abs_path == Path("/"):
                raise ValueError(
                    "Project root path cannot resolve to system root '/', "
                    "please specify a valid path via `PROJECT_ROOT_PATH` environment variable."
                )

        return v
