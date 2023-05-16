from flask import Flask, request
import requests, uuid

app = Flask(__name__)

logging_service_url = "http://localhost:5001"
messages_service_url = "http://localhost:5002"

messages = {}


@app.route('/', methods=['GET'])
def do_GET():
    response = {}
    logging_response = requests.get(logging_service_url)
    messages_response = requests.get(messages_service_url)

    if logging_response.status_code == 200:
        response['logging_service'] = logging_response.json()

    if messages_response.status_code == 200:
        response['messages_service'] = messages_response.json()

    return response, 200


@app.route('/', methods=['POST'])
def do_POST():
    msg = request.get_json()
    if msg:
        msg_id = generate_uuid()
        messages[msg_id] = msg

        logging_response = requests.post(logging_service_url, json={'id': msg_id, 'message': msg})

        if logging_response.status_code == 201:
            return "Message received and logged.", 201

    return "Invalid message.", 400


def generate_uuid():
    return str(uuid.uuid4())


if __name__ == '__main__':
    app.run(port=5000)
