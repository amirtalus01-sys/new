import os

from agent_reach.integrations.mcp_server import create_server
from mcp.server.transport_security import TransportSecuritySettings

PUBLIC_HOST = os.environ.get(
    "MCP_PUBLIC_HOST",
    "agent-reach-mcp-production-9da5.up.railway.app",
)

server = create_server()
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
