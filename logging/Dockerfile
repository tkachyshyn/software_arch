FROM python
WORKDIR /usr/src/log
COPY . .

CMD uvicorn LoggingController:controller.app --port 8080 --host 0.0.0.0