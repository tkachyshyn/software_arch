from Message import Message
import requests
import random
import hazelcast
import consul
import os
import socket
import json
class FacadeService:
    def __init__(self):

        self.client = hazelcast.HazelcastClient(cluster_members=["hazelcast1"])
        self.id = os.environ["SERVICE_ID"]
        self.name = "facade"
        self.consul_service = consul.Consul(host="consul")
        hostname = socket.gethostname()
        check = consul.Check.http(f"http://{hostname}:8080/health", "10s", "2s", "20s")
        self.consul_service.agent.service.register(self.name, service_id=self.name + self.id, address=hostname,
                                                   port=8080, check=check)
        self.mq_queue = self.client.get_queue(self.consul_service.kv.get('queue-name')[1]["Value"].decode('utf-8'))

        self.endpoints = {
            "logging": "/log",
            "messages": "/messages"
        }
        self.ports = {
            "logging": 8080,
            "messages": 8080
        }


    def choose_random_service(self, services_list: list, already_used=None):
        if already_used is None:
            already_used = []
        service = services_list[random.randint(0, len(services_list) - 1)]
        while service in already_used:
            service = services_list[random.randint(0, len(services_list) - 1)]
        return service

    def get_service_addr_from_consul(self, name):
        srv = self.consul_service.health.service(name)[1]
        srv = random.choice(srv)["Service"]
        addr, port = srv["Address"], srv["Port"]
        return f"http://{addr}:{port}{self.endpoints[name]}"


class FacadeController:
    def __init__(self):
        self.app = FastAPI()

        self.facade_service = FacadeService()

        @self.app.get("/log", response_class=PlainTextResponse)
        def get_messages():
            service = self.facade_service.get_service_addr_from_consul("logging")
            r_logging = requests.get(service)
            while r_logging.status_code != 200:
                print(r_logging.status_code)
                service = self.facade_service.get_service_addr_from_consul("logging")
                r_logging = requests.get(service)
            messages = r_logging.json()

            service = self.facade_service.get_service_addr_from_consul("messages")
            r_messages = requests.get(service)
            while r_messages.status_code != 200:
                print(r_messages.status_code)
                service = self.facade_service.get_service_addr_from_consul("messages")
                r_messages = requests.get(service)

            print(r_messages.text)
            print(str(messages), r_messages.text)
            return (str(messages).replace("[", "").replace("]", '').replace("\'", "")) + "\n" + (
                str(r_messages.text).replace("[", "").replace("]", '').replace("\'", ""))

        @self.app.post("/log")
        def post_msg(msg: Message):
            msg.msg_uuid = uuid.uuid1()
            service_chosen = self.facade_service.choose_random_service(self.facade_service.logging_services)
            used = [service_chosen]
            print("service_chosen: ", service_chosen)
            r_logging = requests.post(service_chosen, data=msg.json())
            print(r_logging.status_code)

            while r_logging.status_code != 200:
                service_chosen = self.facade_service.choose_random_service(self.facade_service.logging_services, used)
                print(service_chosen)
                r_logging = requests.post(service_chosen, data=msg.json())
                print(r_logging.status_code)
                used.append(service_chosen)

            while True:
                if self.facade_service.mq_queue.offer(msg.msg).result():
                    break
            return


controller = FacadeController()

if __name__ == "__main__":
    uvicorn.run(controller.app)