from pydantic import BaseModel

from requests.models import PreparedRequest

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response

from fastapi.templating import Jinja2Templates

from starlette.responses import RedirectResponse

import traceback

import app.utils.pass_util as pass_util
from app.common.config import *

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

class EncryptResponse(BaseModel):
  token_version_id: str
  enc_data: str
  integrity_value: str

class DecryptRequest(BaseModel):
  token_version_id: str
  enc_data: str
  integrity_value: str

@router.get('/encrypt/data')
async def nice_encrypt(req: Request, returnUrl: str, redirectUrl: str):

  try:
    result = pass_util.encrypt_request_data(returnUrl)

    req.session["redirectUrl"] = redirectUrl

    # 복호화를 위해, 암호화 키를 세션에 저장
    req.session["_nice_key"] = result["key"]
    req.session["_nice_iv"] = result["iv"]
    req.session["_nice_req_no"] = result["req_no"]
    req.session["_nice_period"] = result["period"]
    req.session["_nice_time"] = result["timestamp"]

    print(result["key"])
    print(result["iv"])
  except Exception as e:
    err_msg = traceback.format_exc()
    print(err_msg)
    raise HTTPException(400, str(e))

  res = {
    "request": req,
    "enc_data": result["request_data"]["enc_data"],
    "token_version_id": result["request_data"]["token_version_id"],
    "integrity_value": result["request_data"]["integrity_value"]
  }

  #return EncryptResponse(**result["request_data"])
  return templates.TemplateResponse("submit.html", res)

@router.post('/decrypt/data')
async def nice_decrypt_post(req: Request, body: DecryptRequest, response: Response):

  try:
    key = req.session.get("_nice_key")
    iv = req.session.get("_nice_iv")
    req_no = req.session.get("_nice_req_no")
    period = req.session.get("_nice_period")
    timestamp = req.session.get("_nice_time")

    if key is None or iv is None or req_no is None or period is None or timestamp is None:
        raise HTTPException(400, "세션이 만료되었습니다.")

    redirectUrl = req.session.get("redirectUrl")

    if redirectUrl is None:
        raise HTTPException(400, "세션이 만료되었습니다.")

    enc_data = body.enc_data

    result = pass_util.decrypt_response_data(enc_data, key, iv)

  except Exception as e:
    err_msg = traceback.format_exc()
    print(err_msg)

    response.delete_cookie('session')
    headers = {"set-cookie": response.headers['set-cookie']}
    raise HTTPException(400, str(e), headers=headers)

  if result['requestno'] != req_no:
    raise HTTPException(400, '요청 번호가 일치하지 않습니다.')

  if not pass_util.is_token_valid(period, timestamp):
    raise HTTPException(401, '토큰이 만료되었습니다. 다시 시도하세요.')


  temp = PreparedRequest()
  temp.prepare_url(redirectUrl, result)
  url = temp.url

  res = RedirectResponse(url=url if url else redirectUrl)

  return res

@router.get('/decrypt/data')
async def nice_decrypt_get(
    req: Request,
    token_version_id: str,
    enc_data: str,
    integrity_value: str,
    response: Response
  ):

  try:
    key = req.session.get("_nice_key")
    iv = req.session.get("_nice_iv")
    req_no = req.session.get("_nice_req_no")
    period = req.session.get("_nice_period")
    timestamp = req.session.get("_nice_time")

    if key is None or iv is None or req_no is None or period is None or timestamp is None:
      raise HTTPException(400, "세션이 만료되었습니다.")

    redirectUrl = req.session.get("redirectUrl")

    if redirectUrl is None:
      raise HTTPException(400, "세션이 만료되었습니다.")

    result = pass_util.decrypt_response_data(enc_data, key, iv)

  except Exception as e:
    err_msg = traceback.format_exc()
    print(err_msg)

    response.delete_cookie('session')
    headers = {"set-cookie": response.headers['set-cookie']}
    raise HTTPException(400, str(e), headers=headers)

  if result['requestno'] != req_no:
    raise HTTPException(400, '요청 번호가 일치하지 않습니다.')

  if not pass_util.is_token_valid(period, timestamp):
    raise HTTPException(401, '토큰이 만료되었습니다. 다시 시도하세요.')

  temp = PreparedRequest()
  temp.prepare_url(redirectUrl, result)
  url = temp.url

  res = RedirectResponse(url=url if url else redirectUrl)

  return res
