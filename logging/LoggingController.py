from fastapi import FastAPI
from Message import Message
import hazelcast
import hazelcast
import consul
import os
import socket


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
        self.logging_repository = LoggingHazelRepository()
        self.id = os.environ["SERVICE_ID"]
        self.name = "logging"
        self.consul_service = consul.Consul(host="consul")
        hostname = socket.gethostname()
        check = consul.Check.http(f"http://{hostname}:8080/health", "10s", "2s", "20s")
        self.consul_service.agent.service.register(self.name, service_id=self.name + self.id, address=hostname,
                                                   port=8080, check=check)
        self.logging_repository.add_map_name(self.consul_service.kv.get('map-name')[1]["Value"].decode('utf-8'))

    def log_new_message(self, msg: Message):
        self.logging_repository.lock(msg.msg_uuid)
        self.logging_repository.put(msg.msg_uuid, msg.msg).result()
        self.logging_repository.unlock(msg.msg_uuid)

    def get_all_messages(self):
        return list(self.logging_repository.values().result())


controller = LoggingController()