from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def do_GET():
    return "not implemented yet", 200

if __name__ == '__main__':
    app.run(port=5002)
