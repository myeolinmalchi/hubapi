import requests

from app.models.sms import *

from app.common.config import *
from common import *


def send_message(body: SMSRequestBody) -> SMSResponseBody:
  '''메세지 발송'''
  data = dict(body)

  uri = f"/sms/v2/services/{NCP_SMS_SERVICE_ID}/messages"
  headers = get_request_headers(uri, "POST")

  res = requests.post(
    f"{NCP_SMS_API_URL}/{uri}",
    headers=headers,
    json=data,
  )

  res.raise_for_status()

  result = res.json()

  return SMSResponseBody(**result)

def check_message_request(params: GetMessageRequestParams) -> GetMessageResponseBody:
  '''메시지 발송 요청 조회'''
  _params = dict(params)

  uri = f"/sms/v2/services/{NCP_SMS_SERVICE_ID}/messages"
  headers = get_request_headers(uri, "GET")

  res = requests.get(
    f"{NCP_SMS_API_URL}/{uri}",
    headers=headers,
    params=_params
  )

  res.raise_for_status()

  result = res.json()

  return GetMessageResponseBody(**result)

def check_message_result(messageId: int) -> CheckMessageResponseBody:
  '''메시지 발송 결과 조회'''

  uri = f"/sms/v2/services{NCP_SMS_SERVICE_ID}/messages/{messageId}"
  headers = get_request_headers(uri, "GET")

  res = requests.get(
    f"{NCP_SMS_API_URL}/{uri}",
    headers=headers,
  )

  res.raise_for_status()

  result = res.json()

  return CheckMessageResponseBody(**result)

def check_message_reservation(reserveId: int) -> CheckMessageReservationBody:
  '''예약 메시지 상태 조회'''

  uri = f"/sms/v2/services/{NCP_SMS_SERVICE_ID}/reservations/{reserveId}/reserve-status"
  headers = get_request_headers(uri, "GET")
  
  res = requests.get(
    f"{NCP_SMS_API_URL}/{uri}",
    headers=headers,
  )

  res.raise_for_status()

  result = res.json()

  return CheckMessageReservationBody(**result)

def cancel_message_reservation(reserveId: int) -> requests.Response:
  '''예약 메시지 취소'''

  uri = f"/sms/v2/services/{NCP_SMS_SERVICE_ID}/reservations/{reserveId}/reserve-status"
  headers = get_request_headers(uri, "GET")
  
  res = requests.delete(
    f"{NCP_SMS_API_URL}/{uri}",
    headers=headers,
  )

  res.raise_for_status()

  return res
