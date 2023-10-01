import time
from typing import Dict

import jwt
from app.common.config import ACCESS_SECRET_KEY

def token_response(token: str):
  return {
    "access_token": token
  }


def signJWT(user_id: str) -> Dict[str, str]:
  payload = {
    "user_id": user_id,
    "expires": time.time() + 600
  }
  token = jwt.encode(payload, ACCESS_SECRET_KEY, algorithm="HS256")

  return token_response(token)


def decodeJWT(token: str):
  try:
    decoded_token = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=["HS256"])
    return decoded_token if decoded_token["exp"] >= time.time() else None
  except:
    return {}
