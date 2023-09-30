from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from app.common.config import *
import requests

router = APIRouter()

@router.get("/oauth")
def oauth(code: str, state: str, error: str | None = None):
  url = f"{MODUSIGN_API_URL}/oauth/token"
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  body = {
    "grant_type": "authorization_code",
    "client_id": MODUSIGN_CLIENT_ID,
    "client_secret": MODUSIGN_CLIENT_SECRET,
    "code": code,
    "redirect_uri": MODUSIGN_REDIRECT_URI
  }

  res = requests.post(
    url=url,
    json=body,
    headers=headers
  )

  return JSONResponse(res.json(), res.status_code)

class RefreshRequest(BaseModel):
  refresh_token: str

@router.post("/oauth/refresh")
def refresh(body: RefreshRequest):
  ''''''
  url = f"{MODUSIGN_API_URL}/oauth/token"
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }
  
  _body = {
    "grant_type": "refresh_token",
    "client_id": MODUSIGN_CLIENT_ID,
    "client_secret": MODUSIGN_CLIENT_SECRET,
    "refresh_token": body.refresh_token
  }

  res = requests.post(
    url=url,
    json=_body,
    headers=headers
  )

  return JSONResponse(res.json(), res.status_code)
