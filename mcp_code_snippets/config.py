import json
from typing import Optional

from fastmcp.utilities.mcp_config import MCPConfig

from mcp_code_snippets.settings import get_default_mcp_config


def read_mcp_config(config_path: Optional[str]) -> MCPConfig:
    """Read the MCP configuration from a file.

    Args:
        config_path (str): Path to the MCP configuration file. Default: "mcp_proxy.json".

    Returns:
        MCPConfig: The MCP configuration object.
    """

    if config_path is None:
        return get_default_mcp_config()

    with open(config_path, "r") as f:
        raw_config = json.load(f)

    if not isinstance(raw_config, dict):
        raise ValueError("Config file must be a JSON object")

    if not raw_config:
        raise ValueError("Config file must have at least one server")

    config = MCPConfig.from_dict(raw_config)

    return config
