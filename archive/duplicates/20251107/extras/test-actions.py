import os
os.environ['NEO_DB_PATH'] = '/tmp/neo_test.sqlite3'
os.environ['ACTIONS_API_KEY'] = 'test-key'

from fastapi.testclient import TestClient
from actions.app import app

client = TestClient(app)

headers = {'x-api-key': 'test-key'}

def test_plan_create():
    r = client.post('/plan_create', json={'goal':'test goal'}, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data['goal'] == 'test goal'
    assert 'milestones' in data

def test_research_web():
    r = client.post('/research_web', json={'queries':['open source ai'], 'max_results':1}, headers=headers)
    assert r.status_code == 200
    assert 'items' in r.json()

def test_fetch_url():
    r = client.post('/fetch_url', json={'url':'https://example.com'}, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert 'url' in data

def test_code_generate():
    r = client.post('/code_generate', json={'language':'python','spec':'print hello'}, headers=headers)
    assert r.status_code == 200
    assert 'code' in r.json()

def test_file_write(tmp_path):
    path = f"/tmp/{'file.txt'}"
    r = client.post('/file_write', json={'path': path, 'content': 'hello'}, headers=headers)
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_task_update():
    r = client.post('/task_update', json={'status':'planned','message':'ok'}, headers=headers)
    assert r.status_code == 200
    assert r.json()['ok'] is True

def test_request_human_approval():
    r = client.post('/request_human_approval', json={'decision':'danger','recommended':'abort'}, headers=headers)
    assert r.status_code == 200
    assert r.json()['requires_human'] is True