FROM docker
WORKDIR /usr/src/facade
COPY . .

CMD uvicorn FacadeController:controller.app --port 8080 --host 0.0.0.0