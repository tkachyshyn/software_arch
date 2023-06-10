from pydantic import BaseModel


class Message(BaseModel):
    msg: str
    msg_uuid: str

class MessagesMemRepository:
    def __init__(self):
        self.messages = []
