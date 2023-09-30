from typing import Literal 
from pydantic import BaseModel

class SMSRequestBody(BaseModel):
  subject: str
  content: str
  sender: str
  receivers: list[str]
  type: Literal['SMS', 'LMS', 'MMS'] = 'SMS'
  contentType: Literal['COMM', 'AD'] = 'COMM'
  reserveTime: str | None = None

  def __dict__(self):
    data = {
      "type": self.type,
      "contentType": self.contentType,
      "from": self.sender,
      "subject": self.subject,
      "content": self.content,
      "messages": [{ "to": receiver } for receiver in self.receivers],
      "reserveTime": self.reserveTime
    }

    return data

class SMSResponseBody(BaseModel):
  requestId: str
  requestTime: str
  statusCode: Literal['202', '400', '401', '403', '404', '429', '500']
  statusName: Literal['success', 'fail']

class GetMessageRequestParams(BaseModel):
  startTime: str
  endTime: str
  sender: str | None = None
  receiver: str | None = None
  status: Literal['SUCCESS', 'FAIL', 'PROCESSING', 'READY', 'ALL'] = 'ALL'
  pageIndex: int = 0
  pageSize: int = 10

  def __dict__(self):
    data = {
      "requestStartTime": self.startTime,
      "requestEndTime": self.endTime,
      "from": self.sender,
      "to": self.receiver,
      "statusName": self.status if self.status is 'SUCCESS' or self.status is 'FAIL' else None,
      "status": self.status if self.status is 'PROCESSING' or self.status is 'READY' else None,
      "pageIndex": self.pageIndex,
      "pageSize": self.pageSize
    }

    return data

class Message(BaseModel):
  requestId: str
  messageId: str
  requestTime: str
  contentType: Literal['COMM', 'AD']
  countryCode: str
  from_: str
  to: str
  status: Literal['READY', 'PROCESSING', 'COMPLETED']

  statusCode: str | None
  statusName: str | None
  statusMessage: str | None
  completeTime: str | None
  telcoCode: str | None

class GetMessageResponseBody(BaseModel):
  statusCode: Literal['200', '400', '401', '403', '404', '500']
  statusName: str

  messages: list[Message]
  pageIndex: int
  pageSize: int
  itemCount: int
  hasMore: bool

class CheckMessageResponseBody(BaseModel):
  statusCode: str
  statusName: str
  messages: list[Message]

class CheckMessageReservationBody(BaseModel):
  reserveId: str
  reserveTime: str
  reserveTime: str
  reserveStatus: str
