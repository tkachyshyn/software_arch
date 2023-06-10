from pydantic import BaseModel


class Message(BaseModel):
    msg: str
    msg_uuid: str = None