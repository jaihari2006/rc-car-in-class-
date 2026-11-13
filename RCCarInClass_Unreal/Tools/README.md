# Unreal Engine 5 MCP (Model Context Protocol) Server

This MCP server provides a direct bridge between **Google Antigravity** and **Unreal Engine 5**. It enables Antigravity to inspect, automate, and control the Unreal Editor using JSON-RPC 2.0 over standard I/O (`stdio`).

---

## Features Exposed to Antigravity

| Tool | Description |
| :--- | :--- |
| `unreal_ping` | Checks connectivity to Unreal Engine's Web Remote Control server (`http://127.0.0.1:30010`). |
| `unreal_execute_console_command` | Executes editor console commands (`stat fps`, `stat unit`, `r.Nanite 1`, `r.Lumen 1`, `RestartLevel`, etc.). |
| `unreal_call_function` | Calls any `UFunction` or BlueprintCallable function on any Actor/Object in the active level. |
| `unreal_get_property` | Reads variables and properties from any Actor or Object in the world. |
| `unreal_set_property` | Modifies properties (speed, transform, nitro amount, colors) in real-time. |
| `unreal_execute_python` | Runs arbitrary Python code inside Unreal Engine's Python runtime to spawn actors, import assets, query levels, etc. |
| `unreal_list_actors` | Lists actors in the active level with optional class filtering. |

---

## Quick Setup

### 1. Requirements
- Python 3.8+ (uses standard library only; **no extra `pip` dependencies needed**).
- Unreal Engine 5.3+ with `RCCarInClass.uproject` opened.
- `PythonScriptPlugin` and `WebRemoteControl` (already configured in `RCCarInClass.uproject` and `DefaultEngine.ini`).

### 2. Verify Unreal Web Remote Control
When Unreal Editor opens the project, the Web Remote Control server runs at:
```text
http://127.0.0.1:30010
```

To verify the MCP server standalone:
```bash
python3 Tools/unreal_mcp_server.py --test
```

### 3. Antigravity Configuration
Copy [mcp_config.json](file:///workspace/bold-faraday/RCCarInClass_Unreal/Tools/mcp_config.json) to your Antigravity config directory:

- **Linux / macOS**: `~/.gemini/config/mcp_config.json`
- **Windows**: `%USERPROFILE%\.gemini\config\mcp_config.json`

Example `mcp_config.json`:
```json
{
  "mcpServers": {
    "unreal-engine": {
      "command": "python",
      "args": [
        "Tools/unreal_mcp_server.py"
      ],
      "env": {
        "UNREAL_ENDPOINT": "http://127.0.0.1:30010"
      }
    }
  }
}
```

Restart or reload Antigravity, and all `unreal_*` tools will be available!
