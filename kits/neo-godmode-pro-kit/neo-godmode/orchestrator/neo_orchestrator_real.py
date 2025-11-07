import os, json, datetime, sqlite3, requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
DB_PATH = os.getenv("NEO_DB_PATH", "neo_store.sqlite3")

conn = sqlite3.connect(DB_PATH)
conn.execute("CREATE TABLE IF NOT EXISTS memory(id INTEGER PRIMARY KEY, ts TEXT, topic TEXT, content TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS artifacts(id INTEGER PRIMARY KEY, ts TEXT, path TEXT, bytes INTEGER, note TEXT)")
conn.commit()

def memory_store(topic: str, content: str):
    conn.execute("INSERT INTO memory(ts, topic, content) VALUES(datetime('now'), ?, ?)", (topic, content))
    conn.commit()

def artifact_store(path: str, content: str, note: str = ""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    conn.execute("INSERT INTO artifacts(ts, path, bytes, note) VALUES(datetime('now'), ?, ?, ?)", (path, len(content.encode('utf-8')), note))
    conn.commit()
    return {"path": path, "bytes": len(content.encode('utf-8'))}

def web_search(query: str, max_results: int = 10):
    if not SERPAPI_KEY:
        return [{"title": "SerpAPI key missing", "link": "", "snippet": "Set SERPAPI_API_KEY"}]
    url = "https://serpapi.com/search.json"
    r = requests.get(url, params={"engine":"google","q":query,"num":max_results,"api_key":SERPAPI_KEY}, timeout=20)
    r.raise_for_status()
    data = r.json()
    results = []
    for item in (data.get("organic_results") or [])[:max_results]:
        results.append({"title": item.get("title"), "link": item.get("link"), "snippet": item.get("snippet")})
    return results

def fetch_url(url: str):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent":"neo-godmode/1.0"})
        r.raise_for_status()
        text = r.text
    except Exception as e:
        return {"url": url, "error": str(e)}
    title = (text.split("<title>")[1].split("</title>")[0] if "<title>" in text and "</title>" in text else url)[:200]
    return {"url": url, "title": title, "content": text[:2000]}

class Agent:
    def __init__(self, name, role, style):
        self.name, self.role, self.style = name, role, style
    def say(self, txt): return f"[{self.name}] {txt}"

class Strategist(Agent):
    def plan(self, goal: str, constraints: List[str], deadline: Optional[str]):
        plan = {
            "goal": goal, "constraints": constraints, "deadline": deadline,
            "milestones": [{"name":"Plan","eta":"+1h"},{"name":"Build","eta":"+1d"},{"name":"Test","eta":"+1d"},{"name":"Deliver","eta":"+2d"}],
            "risks": ["scope creep","unknown deps","time pressure"]
        }
        memory_store("plan", json.dumps(plan))
        return plan

class Researcher(Agent):
    def recon(self, topics: List[str], max_results: int = 8):
        bundle = []
        for t in topics:
            bundle.append({"query": t, "results": web_search(t, max_results)})
        memory_store("research", json.dumps(bundle))
        return bundle

class Engineer(Agent):
    def build(self, language: str, spec: str, include_tests: bool = True):
        code = f"# {language} prototype by NEO\n# Spec: {spec}\nprint('ok')\n"
        tests = f"# tests\n# assert True\n" if include_tests else ""
        return {"language": language, "code": code, "tests": tests}

class Critic(Agent):
    def review(self, artifact: Dict[str, Any]):
        notes = ["Add error handling","Cover edge cases","README + examples"]
        return {"ok": True, "observations": notes}

class Executor(Agent):
    def deliver(self, path: str, content: str, note: str = ""):
        return artifact_store(path, content, note)

class NEO:
    def __init__(self):
        self.strategist = Strategist("NEO//Strategist","Business & Planning","Decisive")
        self.researcher = Researcher("NEO//Research","R&D Intel","Analytical")
        self.engineer = Engineer("NEO//Engineer","Build & Automate","Precise")
        self.critic = Critic("NEO//Critic","Quality & Risk","Relentless")
        self.executor = Executor("NEO//Executor","Ship & Store","Efficient")

    def run(self, goal: str, constraints: List[str]=None, deadline: Optional[str]=None):
        constraints = constraints or []
        log = []
        plan = self.strategist.plan(goal, constraints, deadline)
        log.append(self.strategist.say("Plan created."))
        recon = self.researcher.recon([goal] + constraints)
        log.append(self.researcher.say("Recon complete."))
        spec = f"{goal}\nConstraints: {constraints}\nSources: {sum(len(x['results']) for x in recon)}"
        artifact = self.engineer.build(language="python", spec=spec, include_tests=True)
        log.append(self.engineer.say("Prototype generated."))
        review = self.critic.review(artifact)
        log.append(self.critic.say("Review complete."))
        payload = artifact["code"] + ("\n\n" + artifact["tests"] if artifact.get("tests") else "")
        delivery = self.executor.deliver("deliverables/neo_proto.py", payload, "first cut")
        log.append(self.executor.say(f"Delivered {delivery['path']} ({delivery['bytes']} bytes)."))
        return {"plan": plan, "recon": recon, "artifact": artifact, "review": review, "delivery": delivery, "log": log}

if __name__ == "__main__":
    neo = NEO()
    out = neo.run("CLI text summarizer MVP", ["portable","tested"])
    print(json.dumps(out, indent=2))