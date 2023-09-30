from fastapi import APIRouter, Depends, HTTPException
from app.models.sms import *

from app.utils.auth.auth_bearer import JWTBearer

import app.utils.sms as sms

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
async def send_message(body: SMSRequestBody) -> SMSResponseBody:
  '''메세지 발송'''
  try:
    res = sms.send_message(body)
    return res
  except Exception as e:
    raise HTTPException(400, e)

@router.get("/requests", dependencies=[Depends(JWTBearer())])
async def check_message_request(query_params: GetMessageRequestParams = Depends()) -> GetMessageResponseBody:
  '''메세지 발송 요청 조회'''
  try:
    res = sms.check_message_request(query_params)
    return res
  except Exception as e:
    raise HTTPException(400, e)

@router.get("/{messageId}", dependencies=[Depends(JWTBearer())])
async def check_message_result(messageId: int) -> CheckMessageResponseBody:
  '''메세지 발송 결과 조회'''
  try:
    res = sms.check_message_result(messageId)
    return res
  except Exception as e:
    raise HTTPException(400, e)

@router.get("/reservations/{reserveId}", dependencies=[Depends(JWTBearer())])
async def check_message_reservation(reserveId: int) -> CheckMessageReservationBody:
  '''예약 메세지 상태 조회'''
  try:
    res = sms.check_message_reservation(reserveId)
    return res
  except Exception as e:
    raise HTTPException(400, e)

@router.get("/reservations/{reserveId}", dependencies=[Depends(JWTBearer())])
async def cancel_message_reservation(reserveId: int):
  '''예약 메시지 취소'''
  try:
    res = sms.cancel_message_reservation(reserveId)
    return res
  except Exception as e:
    raise HTTPException(400, e)
