from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import time, os, json
from threading import Lock, Thread
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64

app = FastAPI(title="NEO JWKS", version="1.0")
lock = Lock()
state = {"keys": [], "active_kid": None, "last_rot": 0}

ROTATE_HOURS = int(os.getenv("JWKS_ROTATE_HOURS","24"))
KID_PREFIX = os.getenv("JWKS_KID_PREFIX","neo-key-")

def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

def gen_keypair() -> Dict[str, Any]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub = key.public_key()
    nums = pub.public_numbers()
    n = b64url(nums.n.to_bytes((nums.n.bit_length() + 7) // 8, "big"))
    e = b64url(nums.e.to_bytes((nums.e.bit_length() + 7) // 8, "big"))
    kid = f"{KID_PREFIX}{int(time.time())}"
    return {
        "kid": kid,
        "priv_pem": priv_pem.decode(),
        "jwk": {"kty":"RSA","kid":kid,"use":"sig","alg":"RS256","n":n,"e":e}
    }

def rotate_if_needed():
    with lock:
        now = time.time()
        if now - state["last_rot"] > ROTATE_HOURS * 3600 or not state["keys"]:
            kp = gen_keypair()
            state["keys"] = [kp] + state["keys"][:1]  # keep previous for grace
            state["active_kid"] = kp["kid"]
            state["last_rot"] = now

def rotator_thread():
    while True:
        rotate_if_needed()
        time.sleep(300)

@app.on_event("startup")
def on_start():
    Thread(target=rotator_thread, daemon=True).start()

@app.get("/.well-known/jwks.json")
def jwks():
    rotate_if_needed()
    return {"keys": [k["jwk"] for k in state["keys"]]}

@app.get("/active-kid")
def active():
    rotate_if_needed()
    return {"kid": state["active_kid"]}