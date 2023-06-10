FROM python
WORKDIR /usr/src/msg
COPY . .

CMD uvicorn MessagesController:controller.app --port 8080 --host 0.0.0.0