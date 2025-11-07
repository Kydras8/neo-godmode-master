# Simple long-task worker using Redis list as a queue
import os, time, json, redis, pathlib

REDIS_HOST = os.getenv("REDIS_HOST","redis")
REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
QUEUE = os.getenv("QUEUE_NAME","neo-tasks")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

print("[worker] listening on", QUEUE)
pathlib.Path("/deliverables").mkdir(parents=True, exist_ok=True)

while True:
    item = r.blpop(QUEUE, timeout=5)
    if not item:
        continue
    _, payload = item
    try:
        job = json.loads(payload)
        jid = job.get("id","no-id")
        task = job.get("task","noop")
        time.sleep(2)
        out_path = f"/deliverables/worker_{jid}.txt"
        with open(out_path,"w") as f:
            f.write(json.dumps({"ok":True,"task":task,"jid":jid}, indent=2))
        print("[worker] done", jid, "->", out_path)
    except Exception as e:
        print("[worker] error:", e)