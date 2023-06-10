from fastapi.responses import PlainTextResponse
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
import hazelcast
from Message import MessagesMemRepository


class MessagesService:
    def __init__(self):
        self.repository = MessagesMemRepository()
        self.client = hazelcast.HazelcastClient(cluster_members=["hazelcast1"])
        self.mq_queue = self.client.get_queue("messages_queue")
        self.loop = asyncio.get_running_loop()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        self.loop.create_task(self.messages_reader())
        yield

    async def messages_reader(self):
        while True:
            if self.mq_queue.is_empty().result():
                await asyncio.sleep(0.1)
            else:
                msg = self.mq_queue.take().result()
                print(msg)
                self.repository.messages.append(msg)

class MessagesController:
    def __init__(self):
        self.service = MessagesService()

        self.app = FastAPI(lifespan=self.service.lifespan)

        @self.app.get("/messages", response_class=PlainTextResponse)
        def get_messages() -> str:
            print("got request")
            return str(self.service.messages)


controller = MessagesController()
