from fastapi import FastAPI
from Message import Message
import hazelcast


class LoggingController:
    def __init__(self):
        self.app = FastAPI()

        self.logging_service = LoggingService()

        @self.app.get("/log")
        def get_messages():
            print("getting all messages")
            return self.logging_service.get_all_messages()

        @self.app.post("/log")
        def post_message(msg: Message):
            print("message uuid: ", msg.msg_uuid, "\nmessage:   ", msg.msg)
            self.logging_service.log_new_message(msg)


class LoggingService:
    def __init__(self):
        self.logging_repository = hazelcast.HazelcastClient(cluster_members=["hazelcast1"]).get_map("messages-map")

    def log_new_message(self, msg: Message):
        self.logging_repository.lock(msg.msg_uuid)
        self.logging_repository.put(msg.msg_uuid, msg.msg).result()
        self.logging_repository.unlock(msg.msg_uuid)

    def get_all_messages(self):
        return list(self.logging_repository.values().result())


controller = LoggingController()