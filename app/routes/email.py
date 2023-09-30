from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
import requests
from app.common.config import *

from app.utils.auth.auth_bearer import JWTBearer
from app.utils.common import get_request_headers

router = APIRouter()

@router.post("/mails", dependencies=Depends(JWTBearer()))
async def send_email(req: Request):
  body = await req.json()
  uri = f"/mails"
  headers = get_request_headers(uri, "POST")
  res = requests.post(f"{NCP_EMAIL_API_URL}/{uri}", json=body, headers=headers)
  return JSONResponse(res.json(), res.status_code)

@router.get("/mails/requests", dependencies=Depends(JWTBearer()))
async def check_mail_request(req: Request):
  params = req.query_params
  uri = f"/mails/requests"
  headers = get_request_headers(uri, "GET")
  res = requests.post(f"{NCP_EMAIL_API_URL}/{uri}", params=params, headers=headers)
  return JSONResponse(res.json(), res.status_code)

@router.get("/mails/requests/{requestId}/mails", dependencies=Depends(JWTBearer()))
async def check_mail_list(requestId: int, req: Request):
  params = req.query_params
  uri = f"/mails/requests/{requestId}/mails"
  headers = get_request_headers(uri, "GET")
  res = requests.post(f"{NCP_EMAIL_API_URL}/{uri}", params=params, headers=headers)
  return JSONResponse(res.json(), res.status_code)
