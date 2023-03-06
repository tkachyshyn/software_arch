from flask import Flask


app = Flask(__name__)
host_name = "localhost"
host_port = 5002

@app.get("/")
def do_GET():
    return 'message'

if __name__ == "__main__":
    app.run(host_name, host_port)
