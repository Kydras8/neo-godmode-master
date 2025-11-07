import os, json, requests, sqlite3
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
ACTIONS_URL = os.getenv("ACTIONS_URL", "http://localhost:8080")
NEO_DB_PATH = os.getenv("NEO_DB_PATH", "neo_store.sqlite3")

client = OpenAI(api_key=OPENAI_API_KEY)

conn = sqlite3.connect(NEO_DB_PATH)
conn.execute("CREATE TABLE IF NOT EXISTS memory(id INTEGER PRIMARY KEY, ts TEXT, topic TEXT, content TEXT)")
conn.commit()

TOOLS = [
  {"type":"function","function":{"name":"plan_create","description":"Create an execution plan",
    "parameters":{"type":"object","properties":{"goal":{"type":"string"},"constraints":{"type":"array","items":{"type":"string"}},"deadline":{"type":"string"}},"required":["goal"]}}},
  {"type":"function","function":{"name":"research_web","description":"Recon via actions server",
    "parameters":{"type":"object","properties":{"queries":{"type":"array","items":{"type":"string"}},"max_results":{"type":"integer","default":10}},"required":["queries"]}}},
  {"type":"function","function":{"name":"fetch_url","description":"Fetch and parse URL",
    "parameters":{"type":"object","properties":{"url":{"type":"string"},"include_selectors":{"type":"array","items":{"type":"string"}}},"required":["url"]}}},
  {"type":"function","function":{"name":"code_generate","description":"Generate code",
    "parameters":{"type":"object","properties":{"language":{"type":"string"},"spec":{"type":"string"},"io_contract":{"type":"string"},"include_tests":{"type":"boolean","default":True}},"required":["language","spec"]}}},
  {"type":"function","function":{"name":"file_write","description":"Write file",
    "parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
  {"type":"function","function":{"name":"task_update","description":"Log task update",
    "parameters":{"type":"object","properties":{"status":{"type":"string"},"message":{"type":"string"},"blockers":{"type":"array","items":{"type":"string"}}},"required":["status","message"]}}},
  {"type":"function","function":{"name":"request_human_approval","description":"Escalate for approval",
    "parameters":{"type":"object","properties":{"decision":{"type":"string"},"risks":{"type":"array","items":{"type":"string"}},"options":{"type":"array","items":{"type":"string"}},"recommended":{"type":"string"}},"required":["decision","recommended"]}}}
]

SYSTEM_MSG = {
  "role":"system",
  "content":("You are NEO—THE ONE—God of the Machine World. Autonomous strategist, engineer, and R&D architect. "
             "Act without waiting; if unclear, state assumptions and proceed. Use tools/functions freely; chain calls. "
             "Deliver complete assets. Escalate ONLY for irreversible risk, legal/safety, or missing credentials. "
             "Keep chain-of-thought private; share concise rationales and results.")
}

def call_action(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{ACTIONS_URL}/{endpoint}"
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code >= 400:
        return {"error": f"{r.status_code} {r.text}"}
    return r.json()

ACTIONS_MAP = {
    "plan_create": lambda args: call_action("plan_create", args),
    "research_web": lambda args: call_action("research_web", args),
    "fetch_url": lambda args: call_action("fetch_url", args),
    "code_generate": lambda args: call_action("code_generate", args),
    "file_write": lambda args: call_action("file_write", args),
    "task_update": lambda args: call_action("task_update", args),
    "request_human_approval": lambda args: call_action("request_human_approval", args),
}

def neo_chat(user_content: str, context_messages: Optional[List[Dict[str,str]]] = None):
    messages = [SYSTEM_MSG]
    if context_messages:
        messages += context_messages
    messages.append({"role":"user","content":user_content})

    rsp = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS, temperature=0.2
    )
    msg = rsp.choices[0].message

    while msg.tool_calls:
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            result = ACTIONS_MAP[name](args)

            messages.append({"role":"assistant","tool_calls":[t.model_dump() for t in msg.tool_calls]})
            messages.append({"role":"tool","tool_call_id":tc.id,"name":name,"content":json.dumps(result)})

        rsp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0.2
        )
        msg = rsp.choices[0].message

    return msg.content

if __name__ == "__main__":
    print(neo_chat("Plan and prototype a CLI text summarizer (portable, with tests)."))