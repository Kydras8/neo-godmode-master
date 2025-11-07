# Mint a JWT with scopes
import os, time, jwt, json
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv("JWT_SECRET","dev-secret")
alg = os.getenv("JWT_ALG","HS256")
iss = os.getenv("JWT_ISS","neo-actions")
aud = os.getenv("JWT_AUD","neo-clients")

scopes = (os.getenv("DEFAULT_SCOPES","") or "").split(",")
claims = {
  "iss": iss,
  "aud": aud,
  "iat": int(time.time()),
  "exp": int(time.time()) + 3600,
  "scopes": scopes
}

tok = jwt.encode(claims, secret, algorithm=alg)
print(json.dumps({"token": tok, "claims": claims}, indent=2))