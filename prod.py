import flask
from core.logger import Logger

app = flask.Flask("prod")
log = Logger("prod")

@app.route('/api')
def main():
    msg = flask.request.args.get('message')
    log.info(f"Received message: {msg}")
    return msg

if __name__ == "__main__":
    app.run(debug=True, port=9000)