from flask import Flask, request

app = Flask(__name__)
host_name = "localhost"
host_port = 5001
messages = dict()

@app.get("/")
def do_GET():
    return str(list(messages.items()))

@app.post("/")
def do_POST():
    uid = request.form['id']
    print(uid)
    messages[uid] = request.form['text']
    return ''

if __name__ == '__main__':
    app.run(host_name, host_port)
