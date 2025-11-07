from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import os, json, datetime, requests, sqlite3

app = FastAPI(title="NEO Actions", version="1.0.0")

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("ACTIONS_API_KEY")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if API_KEY and x_api_key == API_KEY:
        return True
    if not API_KEY:
        # If no API key set, allow but warn
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")


DB_PATH = os.getenv("NEO_DB_PATH", "/data/neo_store.sqlite3")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute(    "CREATE TABLE IF NOT EXISTS memory(id INTEGER PRIMARY KEY, ts TEXT, topic TEXT, content TEXT)")
conn.execute(    "CREATE TABLE IF NOT EXISTS artifacts(id INTEGER PRIMARY KEY, ts TEXT, path TEXT, bytes INTEGER, note TEXT)")
conn.commit()

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def memory_store(topic: str, content: str):
    conn.execute("INSERT INTO memory(ts, topic, content) VALUES(datetime('now'), ?, ?)",
                 (topic, content))
    conn.commit()

def artifact_store(path: str, content: str, note: str = ""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    conn.execute("INSERT INTO artifacts(ts, path, bytes, note) VALUES(datetime('now'), ?, ?, ?)",
                 (path, len(content.encode('utf-8')), note))
    conn.commit()
    return {"path": path, "bytes": len(content.encode('utf-8'))}

class PlanCreateIn(BaseModel):
    goal: str
    constraints: Optional[List[str]] = Field(default_factory=list)
    deadline: Optional[str] = None

@app.post("/plan_create")
async def _auth_guard(dep: bool = Depends(verify_api_key)): pass

@app.post("/plan_create")
def plan_create(inp: PlanCreateIn):
    plan = {
        "goal": inp.goal,
        "constraints": inp.constraints,
        "deadline": inp.deadline,
        "milestones": [
            {"name": "Plan", "eta": "+1h", "deliverable": "Execution plan"},
            {"name": "Build", "eta": "+1d", "deliverable": "Prototype"},
            {"name": "Test", "eta": "+1d", "deliverable": "Report"},
            {"name": "Deliver", "eta": "+2d", "deliverable": "Final package"}
        ],
        "risks": ["scope creep", "unknown dependencies", "time constraints"]
    }
    memory_store("plan:"+inp.goal[:64], json.dumps(plan))
    return plan

class ResearchWebIn(BaseModel):
    queries: List[str]
    max_results: Optional[int] = 10

@app.post("/research_web")
async def _auth_guard2(dep: bool = Depends(verify_api_key)): pass

@app.post("/research_web")
def research_web(inp: ResearchWebIn):
    bundle = []
    for q in inp.queries:
        if SERPAPI_KEY:
            url = "https://serpapi.com/search.json"
            r = requests.get(url, params={"engine":"google","q":q,"num":inp.max_results,"api_key":SERPAPI_KEY}, timeout=20)
            items = (r.json().get("organic_results") or [])[:inp.max_results]
            results = [{"title": i.get("title"), "link": i.get("link"), "snippet": i.get("snippet")} for i in items]
        else:
            results = [{"title":"SerpAPI key missing","link":"","snippet":"Set SERPAPI_API_KEY"}]
        bundle.append({"query": q, "results": results})
    memory_store("research", json.dumps(bundle))
    return {"items": bundle}

class FetchUrlIn(BaseModel):
    url: str
    include_selectors: Optional[List[str]] = None

@app.post("/fetch_url")
async def _auth_guard3(dep: bool = Depends(verify_api_key)): pass

@app.post("/fetch_url")
def fetch_url(inp: FetchUrlIn):
    try:
        r = requests.get(inp.url, timeout=20, headers={"User-Agent":"neo-godmode/1.0"})
        r.raise_for_status()
        text = r.text
    except Exception as e:
        return {"url": inp.url, "error": str(e)}
    title = (text.split("<title>")[1].split("</title>")[0] if "<title>" in text and "</title>" in text else inp.url)[:200]
    return {"url": inp.url, "title": title, "summary": text[:2000]}

class CodeGenerateIn(BaseModel):
    language: str
    spec: str
    io_contract: Optional[str] = ""
    include_tests: Optional[bool] = True

@app.post("/code_generate")
async def _auth_guard4(dep: bool = Depends(verify_api_key)): pass

@app.post("/code_generate")
def code_generate(inp: CodeGenerateIn):
    code = f"# {inp.language} prototype by NEO\n# Spec: {inp.spec}\n# IO: {inp.io_contract}\nprint('ok')\n"
    tests = f"# tests for {inp.language}\n# assert True\n" if inp.include_tests else ""
    return {"language": inp.language, "code": code, "tests": tests}

class FileWriteIn(BaseModel):
    path: str
    content: str

@app.post("/file_write")
async def _auth_guard5(dep: bool = Depends(verify_api_key)): pass

@app.post("/file_write")
def file_write(inp: FileWriteIn):
    res = artifact_store(inp.path, inp.content, "action write")
    return {"status": "ok", **res}

class TaskUpdateIn(BaseModel):
    status: str
    message: str
    blockers: Optional[List[str]] = Field(default_factory=list)

@app.post("/task_update")
async def _auth_guard6(dep: bool = Depends(verify_api_key)): pass

@app.post("/task_update")
def task_update(inp: TaskUpdateIn):
    memory_store("task_update", inp.json())
    return {"ok": True, **inp.dict()}

class RequestHumanApprovalIn(BaseModel):
    decision: str
    risks: Optional[List[str]] = Field(default_factory=list)
    options: Optional[List[str]] = Field(default_factory=list)
    recommended: str

@app.post("/request_human_approval")
async def _auth_guard7(dep: bool = Depends(verify_api_key)): pass

@app.post("/request_human_approval")
def request_human_approval(inp: RequestHumanApprovalIn):
    memory_store("approval_request", inp.json())
    return {"requires_human": True, **inp.dict()}