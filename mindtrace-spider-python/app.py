from app import app
from app.service.router import route
from flask import request


@app.route('/debug')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/", methods=["POST"])
def get_website_info():
    try:
        return route(request.json["type"])(request.json["url"])
    except:
        return {"error": "resolve failure"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=34984)
