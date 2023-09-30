from typing import Literal
from pydantic import BaseModel

class RecipientForRequest(BaseModel):
  address: str
  name: str | None = None
  type: Literal['R', 'C', 'B'] = 'R'
  parameters: dict[str, str] | None = None

class RecipientGroupFilter(BaseModel):
  andFilter: bool
  groups: list[str]

class EmailRequestBody(BaseModel):
  senderAddress: str | None = None
  senderName: str | None = None
  templateSid: int | None = None
  title: str | None = None
  body: str | None = None
  individual: bool | None = None
  confirmAndSend: bool | None = None
  advertising: bool | None = None
  parameters: dict[str, str] | None = None
  referencesHeader: bool | None = None
  reservationUtc: int | None = None
  reservationDateTime: str | None = None
  attachFields: list[str] | None = None
  recipients: list[RecipientForRequest] | None = None
  recipientGroupFilter: list[RecipientGroupFilter] | None = None
  unsubscribeMessage: str | None = None

class EmailResponseBody(BaseModel):
  requestId: str
  count: int

class GetMailRequestParams(BaseModel):
  startUtc: int
  startDateTime: str
  endUtc: int
  endDateTime: str
  requestId: str | None = None
  mailId: str | None = None
  dispatchType: Literal['CONSOLE', 'API'] | None = None
  title: str | None = None
  templateSid: int | None = None
  senderAddress: str | None = None
  sendStatus: list[str] | None = None
  size: int | None = None
  sort: Literal['createUtc', 'recipientCount', 'reservationUtc', 'sendUtc', 'statusCode'] | None = None

class Sort(BaseModel):
  direction: Literal['ASC', 'DESC']
  property: str
  ignoreCase: bool
  nullHandling: Literal['NATIVE', 'NULLS_FIRST', 'NULLS_LAST']
  ascending: bool
  descending: bool

class NesDateTime(BaseModel):
  utc: int
  formattedDate: str
  formattedDateTime: str

class EmailStatus(BaseModel):
  label: str
  code: str

class RequestListResponse(BaseModel):
  requestId: str
  templateSid: int | None = None
  templateName: str | None = None
  senderAddress: str | None = None
  dispatchType: Literal['CONSOLE', 'API'] | None = None
  emailStatus: EmailStatus
  requestDate: NesDateTime

class EmailReservationStatus(BaseModel):
  label: str
  code: Literal['Y', 'N']

class MailListResponse(BaseModel):
  mailId: str
  templateSid: int | None = None
  templateName: str | None = None
  senderAddress: str
  senderName: str | None = None
  title: str
  emailStatus: EmailStatus
  requestDate: NesDateTime
  sendDate: NesDateTime | None = None
  reservationStatus: EmailReservationStatus
  advertising: bool
  representativeRecipient: str

class GetMailResponseBody(BaseModel):
  totalElements: int
  totalPages: int
  numberOfElements: int
  first: bool
  last: bool
  number: int
  size: int
  sort: list[Sort]
  content: list[MailListResponse] | None = None
