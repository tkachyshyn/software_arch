from flask import Flask, jsonify, request

app = Flask(__name__)

messages = {}


@app.route('/', methods=['GET'])
def do_GET():
    return jsonify(messages), 200


@app.route('/', methods=['POST'])
def do_POST():
    data = request.get_json()
    if data and 'id' in data and 'message' in data:
        msg_id = data['id']
        msg = data['message']
        messages[msg_id] = msg
        print(f"Received message: {msg_id} - {msg}")
        return "Message logged.", 201

    return "Invalid request.", 400


if __name__ == '__main__':
    app.run(port=5001)
