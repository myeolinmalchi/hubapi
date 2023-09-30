from fastapi import FastAPI
from .sms import router as sms_router
from .modusign import router as modusign_router
from .email import router as email_router

app = FastAPI()

app.include_router(sms_router, prefix="/messages")
app.include_router(modusign_router, prefix="/modusign")
app.include_router(email_router, prefix="/mails")
