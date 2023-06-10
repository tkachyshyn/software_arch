import uuid
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from Message import Message
import uvicorn
import requests
import random
import hazelcast


class FacadeService:
    def __init__(self):
        self.logging_services = ["http://logging-service1:8080/log",
                                 "http://logging-service2:8080/log",
                                 "http://logging-service3:8080/log"]

        self.messages_services = ["http://messages-service1:8080/messages",
                                  "http://messages-service2:8080/messages"]

        self.mq_queue = self.hazelcast.HazelcastClient(cluster_members=["hazelcast1"]).get_queue("messages_queue")
    def choose_service(self, lst, used=None):
        if used is None:
            used = []
        service = lst[random.randint(0, len(lst) - 1)]
        while service in used:
            service = lst[random.randint(0, len(lst) - 1)]
        return service


class FacadeController:
    def __init__(self):
        self.app = FastAPI()

        self.facade_service = FacadeService()

        @self.app.get("/log", response_class=PlainTextResponse)
        def get_messages():
            service = self.facade_service.choose_service(self.facade_service.logging_services)
            r_logging = requests.get(service)
            used = [service]
            while r_logging.status_code != 200:
                print(r_logging.status_code)
                service = self.facade_service.choose_service(self.facade_service.logging_services, used)
                r_logging = requests.get(service)
                used.append(service)
            messages = r_logging.json()

            used = []
            service = self.facade_service.choose_service(self.facade_service.messages_services)
            used.append(service)
            rand_msg = requests.get(service)
            while rand_msg.status_code != 200:
                print(rand_msg.status_code)
                service = self.facade_service.choose_service(self.facade_service.messages_services, used)
                rand_msg = requests.get(service)
                used.append(service)

            print(rand_msg.text)
            print(str(messages), rand_msg.text)
            return (str(messages).replace("[", "").replace("]", '').replace("\'", "")) + "\n" + (
                str(rand_msg.text).replace("[", "").replace("]", '').replace("\'", ""))

        @self.app.post("/log")
        def post_msg(msg: Message):
            msg.msg_uuid = uuid.uuid1()
            service = self.facade_service.choose_service(self.facade_service.logging_services)
            used = [service]
            print("service: ", service)
            r_logging = requests.post(service, data=msg.json())
            print(r_logging.status_code)

            while r_logging.status_code != 200:
                service = self.facade_service.choose_service(self.facade_service.logging_services, used)
                print(service)
                r_logging = requests.post(service, data=msg.json())
                print(r_logging.status_code)
                used.append(service)

            while True:
                if self.facade_service.mq_queue.offer(msg.msg).result():
                    break
            return


controller = FacadeController()

if __name__ == "__main__":
    uvicorn.run(controller.app)