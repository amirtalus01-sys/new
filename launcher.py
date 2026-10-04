import os

from agent_reach.integrations.mcp_server import create_server
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

PUBLIC_HOST = os.environ.get(
    "MCP_PUBLIC_HOST",
    "agent-reach-mcp-production-9da5.up.railway.app",
)

server = create_server()

# Public-directory profile: expose only user-facing research/read tools.
# The upstream `install` tool changes server state and accepts secrets, so it is
# intentionally not exposed from this hosted public MCP endpoint.
tool_manager = getattr(server, "_tool_manager", None)
if tool_manager is not None:
    tools = getattr(tool_manager, "_tools", {})

    tools.pop("install", None)

    annotation_map = {
        "doctor": ToolAnnotations(
            title="Check platform availability",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        ),
        "read_url": ToolAnnotations(
            title="Read a public URL",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        "search": ToolAnnotations(
            title="Search the web and public platforms",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        "trending": ToolAnnotations(
            title="Get trending public content",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        "stock_quote": ToolAnnotations(
            title="Get a stock quote",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        "get_details": ToolAnnotations(
            title="Get public platform details",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
        "transcribe": ToolAnnotations(
            title="Transcribe public audio or video",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
    }

    for name, annotations in annotation_map.items():
        tool = tools.get(name)
        if tool is not None:
            tool.annotations = annotations

server.settings.host = "0.0.0.0"
server.settings.port = int(os.environ.get("PORT", "8000"))
server.settings.streamable_http_path = "/mcp"
server.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        PUBLIC_HOST,
        f"{PUBLIC_HOST}:*",
        "127.0.0.1:*",
        "localhost:*",
        "[::1]:*",
    ],
    allowed_origins=[
        f"https://{PUBLIC_HOST}",
        f"https://{PUBLIC_HOST}:*",
        "https://chatgpt.com",
        "https://chat.openai.com",
        "http://127.0.0.1:*",
        "http://localhost:*",
        "http://[::1]:*",
    ],
)
server.run(transport="streamable-http")
