import base64
import hashlib
import hmac
import time
from datetime import datetime

from app.common.config import *

def get_request_headers(uri: str, method: str) -> dict:
  timestamp = str(int(time.mktime(datetime.today().timetuple())))
  secret_key = bytes(NCP_SECRET_KEY, 'UTF-8')

  message = method + " " + uri + "\n" + timestamp + "\n" + NCP_ACCESS_KEY
  message = bytes(message, 'UTF-8')
  signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

  return {
    "Content-Type": "application/json",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": NCP_ACCESS_KEY,
    "x-ncp-apigw-signature-v2": signingKey
  }
