"""Installed `fcc-opencode` launcher for the OpenCode agent client."""

import os
import subprocess
import sys
from collections.abc import Sequence

from free_claude_code.cli.local_http import with_local_proxy_bypass
from free_claude_code.cli.proxy_auth import proxy_auth_token
from free_claude_code.config.server_urls import local_proxy_root_url
from free_claude_code.config.settings import get_settings

from .common import preflight_proxy, resolve_client_binary, run_client_process

_API_KEY_ENV = "FCC_OPENCODE_API_KEY"
_BASE_URL_ENV = "OPENAI_BASE_URL"
_BINARY_NAME = "opencode"
_DISPLAY_NAME = "OpenCode"


def launch(argv: Sequence[str] | None = None) -> None:
    """Launch OpenCode with a process-local Free Claude Code provider."""
    settings = get_settings()
    proxy_root_url = local_proxy_root_url(settings)
    auth_token = proxy_auth_token()

    binary_path = resolve_client_binary(
        binary_name=_BINARY_NAME,
        display_name=_DISPLAY_NAME,
    )

    base_env = dict(os.environ)
    base_env[_BASE_URL_ENV] = f"{proxy_root_url}v1/"
    base_env[_API_KEY_ENV] = auth_token
    base_env["OPENAI_API_KEY"] = auth_token

    run_client_process(
        binary_path,
        argv=list(sys.argv[1:] if argv is None else argv),
        base_env=base_env,
        proxy_url=proxy_root_url,
        auth_token=auth_token,
    )
