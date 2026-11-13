#!/usr/bin/env python3
"""
Unreal Engine 5 MCP (Model Context Protocol) Server
Enables Google Antigravity to inspect, automate, and control Unreal Engine 5 via Web Remote Control & Python Scripting.

No external pip dependencies required (uses standard Python library).
Compatible with Python 3.8+.
"""

import sys
import json
import os
import urllib.request
import urllib.error

DEFAULT_UNREAL_URL = os.environ.get("UNREAL_ENDPOINT", "http://127.0.0.1:30010")

def log(msg):
    sys.stderr.write(f"[UnrealMCP] {msg}\n")
    sys.stderr.flush()

def send_unreal_request(path, method="GET", payload=None, endpoint=None):
    """Sends an HTTP request to Unreal Engine's Web Remote Control API."""
    base_url = (endpoint or DEFAULT_UNREAL_URL).rstrip("/")
    url = f"{base_url}/{path.lstrip('/')}"
    
    headers = {"Content-Type": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            if body:
                try:
                    return {"success": True, "data": json.loads(body), "status": resp.status}
                except json.JSONDecodeError:
                    return {"success": True, "data": body, "status": resp.status}
            return {"success": True, "data": None, "status": resp.status}
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Cannot reach Unreal Engine at {base_url}. Ensure Unreal Editor is running with 'Web Remote Control' plugin enabled. Error: {e}",
            "status": getattr(e, "code", 0)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "status": 0}

TOOLS = [
    {
        "name": "unreal_ping",
        "description": "Check connection to Unreal Engine 5 Web Remote Control server and inspect active session status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "endpoint": {
                    "type": "string",
                    "description": "Optional custom endpoint URL (default: http://127.0.0.1:30010)"
                }
            }
        }
    },
    {
        "name": "unreal_execute_console_command",
        "description": "Execute an Unreal Engine console command (e.g. 'stat fps', 'r.Nanite 1', 'RestartLevel', 'Slomo 0.5', 'ToggleDebugCamera').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The Unreal console command to execute."
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "unreal_call_function",
        "description": "Call a UFunction or BlueprintCallable function on an Actor or Object in the active level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "objectPath": {
                    "type": "string",
                    "description": "Full path to object, e.g. /Game/Maps/ClassroomGym.ClassroomGym:PersistentLevel.RCCarPawn_C_1"
                },
                "functionName": {
                    "type": "string",
                    "description": "Name of the function to call, e.g. ResetVehicle, TriggerNitro, SetSenseiPatrolState"
                },
                "parameters": {
                    "type": "object",
                    "description": "Key-value dictionary of parameters to pass to the function"
                }
            },
            "required": ["objectPath", "functionName"]
        }
    },
    {
        "name": "unreal_get_property",
        "description": "Read a property or variable value from an Actor or UObject in Unreal Engine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "objectPath": {
                    "type": "string",
                    "description": "Object path, e.g. /Game/Maps/ClassroomGym.ClassroomGym:PersistentLevel.RCCarPawn_C_1"
                },
                "propertyName": {
                    "type": "string",
                    "description": "Property name to read, e.g. bNitroActive, CurrentSpeedKPH, NitroFuel"
                }
            },
            "required": ["objectPath", "propertyName"]
        }
    },
    {
        "name": "unreal_set_property",
        "description": "Modify a property or variable on an Actor or UObject in the active level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "objectPath": {
                    "type": "string",
                    "description": "Object path, e.g. /Game/Maps/ClassroomGym.ClassroomGym:PersistentLevel.RCCarPawn_C_1"
                },
                "propertyName": {
                    "type": "string",
                    "description": "Property name to modify"
                },
                "propertyValue": {
                    "description": "New value to assign (scalar, boolean, string, or struct/object)"
                }
            },
            "required": ["objectPath", "propertyName", "propertyValue"]
        }
    },
    {
        "name": "unreal_execute_python",
        "description": "Run Python code directly inside the running Unreal Engine 5 Editor (requires Python Editor Script Plugin). Allows spawning actors, loading levels, creating materials, and querying Unreal classes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python snippet to execute in Unreal Engine's Python runtime."
                }
            },
            "required": ["code"]
        }
    },
    {
        "name": "unreal_list_actors",
        "description": "Query actors present in the currently loaded level, optionally filtered by class name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "className": {
                    "type": "string",
                    "description": "Optional class filter (e.g. 'RCCarPawn', 'TeacherAIController', 'HomeworkPaperPickup', 'StaticMeshActor')"
                }
            }
        }
    }
]

def handle_tool_call(name, args):
    """Executes the tool call and returns the formatted result."""
    if name == "unreal_ping":
        endpoint = args.get("endpoint")
        res = send_unreal_request("remote/info", method="GET", endpoint=endpoint)
        if not res["success"]:
            # Fall back to root check
            res = send_unreal_request("", method="GET", endpoint=endpoint)
            
        if res["success"]:
            return f"Connected to Unreal Engine 5 successfully!\nEndpoint: {endpoint or DEFAULT_UNREAL_URL}\nResponse: {json.dumps(res.get('data'), indent=2)}"
        return f"Failed to connect to Unreal Engine 5.\n{res['error']}"

    elif name == "unreal_execute_console_command":
        cmd = args.get("command")
        payload = {
            "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
            "functionName": "ExecuteConsoleCommand",
            "parameters": {
                "Command": cmd
            },
            "generateTransaction": True
        }
        res = send_unreal_request("remote/object/call", method="PUT", payload=payload)
        if res["success"]:
            return f"Console command '{cmd}' executed successfully.\nResponse: {json.dumps(res.get('data'), indent=2)}"
        return f"Error executing console command: {res['error']}"

    elif name == "unreal_call_function":
        object_path = args.get("objectPath")
        func_name = args.get("functionName")
        parameters = args.get("parameters", {})
        payload = {
            "objectPath": object_path,
            "functionName": func_name,
            "parameters": parameters,
            "generateTransaction": True
        }
        res = send_unreal_request("remote/object/call", method="PUT", payload=payload)
        if res["success"]:
            return f"Function '{func_name}' called on '{object_path}'.\nResult: {json.dumps(res.get('data'), indent=2)}"
        return f"Error calling function: {res['error']}"

    elif name == "unreal_get_property":
        object_path = args.get("objectPath")
        prop_name = args.get("propertyName")
        payload = {
            "objectPath": object_path,
            "propertyName": prop_name,
            "access": "READ_ACCESS"
        }
        res = send_unreal_request("remote/object/property", method="PUT", payload=payload)
        if res["success"]:
            return f"Property '{prop_name}' on '{object_path}':\n{json.dumps(res.get('data'), indent=2)}"
        return f"Error reading property: {res['error']}"

    elif name == "unreal_set_property":
        object_path = args.get("objectPath")
        prop_name = args.get("propertyName")
        prop_val = args.get("propertyValue")
        payload = {
            "objectPath": object_path,
            "propertyName": prop_name,
            "propertyValue": prop_val,
            "access": "WRITE_ACCESS",
            "generateTransaction": True
        }
        res = send_unreal_request("remote/object/property", method="PUT", payload=payload)
        if res["success"]:
            return f"Successfully updated property '{prop_name}' on '{object_path}' to {json.dumps(prop_val)}."
        return f"Error setting property: {res['error']}"

    elif name == "unreal_execute_python":
        code = args.get("code")
        payload = {
            "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
            "functionName": "ExecutePythonCommand",
            "parameters": {
                "PythonCommand": code
            },
            "generateTransaction": True
        }
        res = send_unreal_request("remote/object/call", method="PUT", payload=payload)
        if res["success"]:
            return f"Python code executed successfully in Unreal Engine:\n{json.dumps(res.get('data'), indent=2)}"
        return f"Error executing Python code in Unreal: {res['error']}"

    elif name == "unreal_list_actors":
        class_filter = args.get("className", "")
        # Execute Python snippet via Unreal to query actor list
        py_snippet = f"""
import unreal, json
actors = unreal.EditorLevelLibrary.get_all_level_actors()
results = []
for a in actors:
    name = a.get_name()
    cls = a.get_class().get_name()
    if "{class_filter}" == "" or "{class_filter}".lower() in cls.lower():
        loc = a.get_actor_location()
        results.append({{"name": name, "class": cls, "location": [loc.x, loc.y, loc.z]}})
print("ACTOR_LIST_JSON:" + json.dumps(results[:100]))
"""
        payload = {
            "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
            "functionName": "ExecutePythonCommand",
            "parameters": {
                "PythonCommand": py_snippet
            }
        }
        res = send_unreal_request("remote/object/call", method="PUT", payload=payload)
        if res["success"]:
            return f"Queried actors in level (filter: '{class_filter}'):\n{json.dumps(res.get('data'), indent=2)}"
        return f"Error listing actors: {res['error']}"

    else:
        return f"Unknown tool: {name}"

def send_response(response_dict):
    """Encodes and writes a JSON-RPC response to stdout followed by newline."""
    raw = json.dumps(response_dict)
    sys.stdout.write(raw + "\n")
    sys.stdout.flush()

def run_server():
    """Main JSON-RPC stdio event loop."""
    log("Starting Unreal Engine MCP stdio server...")
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError as err:
                log(f"Failed to decode JSON: {err}")
                continue

            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "unreal-engine-mcp",
                            "version": "1.0.0"
                        }
                    }
                })

            elif method == "notifications/initialized":
                # Notification from client, no response required
                pass

            elif method == "ping":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                })

            elif method == "tools/list":
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS
                    }
                })

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result_text = handle_tool_call(tool_name, tool_args)
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": str(result_text)
                            }
                        ]
                    }
                })

            else:
                # Unknown method
                if req_id is not None:
                    send_response({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method '{method}' not found"
                        }
                    })

        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            log(f"Unhandled server error: {e}")
            if 'req_id' in locals() and req_id is not None:
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Self-test: listing tools...")
        print(f"Total tools defined: {len(TOOLS)}")
        for t in TOOLS:
            print(f" - {t['name']}: {t['description']}")
        print("\nTesting ping fallback when Unreal is offline...")
        print(handle_tool_call("unreal_ping", {}))
        sys.exit(0)
    
    run_server()
