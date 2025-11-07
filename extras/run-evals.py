# Simple eval runner to smoke-test endpoints and measure response shapes/latency
import os, time, json, requests
from dotenv import load_dotenv

load_dotenv()
ACTIONS_URL = os.getenv("ACTIONS_URL", "http://localhost:8080")
API_KEY = os.getenv("ACTIONS_API_KEY", "")

def call(ep, payload):
    t0 = time.time()
    r = requests.post(f"{ACTIONS_URL}/{ep}", json=payload, headers={'x-api-key': API_KEY} if API_KEY else {}, timeout=30)
    dt = time.time() - t0
    return {'status': r.status_code, 'elapsed_s': round(dt,3), 'body': r.json() if r.headers.get('content-type','').startswith('application/json') else r.text}

def main():
    suite = [
        ('plan_create', {'goal':'Eval goal'}),
        ('research_web', {'queries':['open source LLMs'], 'max_results': 2}),
        ('fetch_url', {'url':'https://example.com'}),
        ('code_generate', {'language':'python','spec':'echo hello','include_tests': True}),
        ('file_write', {'path':'/tmp/eval.txt','content':'ok'}),
        ('task_update', {'status':'planned','message':'eval run'}),
        ('request_human_approval', {'decision':'test','recommended':'hold'}),
    ]
    results = {}
    for ep, payload in suite:
        results[ep] = call(ep, payload)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()