import os
import requests

def load_army_rules():
    rules_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '.cursor', 'Neo Godmode Army Rules')
    )
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

ARMY_RULES = load_army_rules()

ACTIONS_URL = os.getenv('ACTIONS_URL', 'http://localhost:8000')
API_KEY = os.getenv('ACTIONS_API_KEY')
JWT = os.getenv('JWT_TOKEN')

def auth_headers():
    if API_KEY:
        return {'x-api-key': API_KEY}
    if JWT:
        return {'Authorization': f'Bearer {JWT}'}
    return {'Content-Type': 'application/json'}

def call_tool(tool, payload):
    url = f"{ACTIONS_URL.rstrip('/')}/{tool}"
    headers = auth_headers()
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error calling {tool}: {e}")
        return {'error': str(e)}

def create_plan(goal):
    return call_tool('plan_create', {'goal': goal})

def research_web(query):
    return call_tool('research_web', {'query': query})

if __name__ == '__main__':
    print('Neo Agent starting...')
    print('Army Rules loaded.' if ARMY_RULES else 'Army Rules not found.')
    try:
        result = create_plan('Build a portable AI agent')
        print('Plan:', result)
    except Exception as e:
        print('Error calling actions service:', e)
