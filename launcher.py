import os

from agent_reach.integrations.mcp_server import create_server

server = create_server()
server.settings.host = "0.0.0.0"
server.settings.port = int(os.environ.get("PORT", "8000"))
server.settings.streamable_http_path = "/mcp"
server.run(transport="streamable-http")
