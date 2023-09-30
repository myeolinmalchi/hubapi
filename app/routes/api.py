from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .sms import router as sms_router
from .modusign import router as modusign_router
from .email import router as email_router
from .pass_api import router as pass_router
from app.common.config import *

app = FastAPI()

app.include_router(sms_router, prefix="/api/messages", tags=["SMS"])
app.include_router(modusign_router, prefix="/api/modusign", tags=["Mail"])
app.include_router(email_router, prefix="/api/mails", tags=["Modusign"])
app.include_router(pass_router, prefix="/nice", tags=["NICE"])

app.add_middleware(SessionMiddleware, secret_key=NICE_SECRET_KEY, https_only=True, same_site="none")

app.add_middleware(
  CORSMiddleware,
  allow_origins = CLIENTS,
  allow_credentials=True,
  allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
  allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin","Set-Cookie"],)

@app.middleware("https")
async def session(req: Request, call_next):
  response = await call_next(req)
  session = req.cookies.get('session')
  if session:
      response.set_cookie(key='session', value=req.cookies.get('session'), httponly=True)
  return response
