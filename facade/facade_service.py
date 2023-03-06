import requests
import uuid
from flask import Flask, request


app = Flask(__name__)

host_name = "localhost"
host_port = 5000
logging_client = "http://localhost:5001"
messages_client = "http://localhost:5002"

@app.get("/")
def do_GET():
    try:
        return f'{requests.get(logging_client).text} | {requests.get(messages_client).text}'
    except requests.exceptions.ConnectionError:
        return "Connection refused"

@app.post("/")
def do_POST():

    return requests.post(logging_client, {'id': uuid.uuid4(), 'text': request.get_json()}).text


if __name__ == '__main__':
    app.run(host_name, host_port, debug=True)
