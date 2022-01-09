from threading import Condition
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify, make_response
import redis
import config

app = Flask("Rate-Limiter")

redis_node = redis.Redis(host=config.REDIS_ENDPOINT, port=config.REDIS_PORT, db=0)


def rate_limit_redis(uid):
    global redis_node
    if redis_node.exists(uid):
        if int(redis_node.get(uid)) + 1 > config.RATE_LIMIT:
            return False
        redis_node.incr(uid)
        return True
    redis_node.set(uid, 0)
    redis_node.expire(uid, config.TTL)
    return True


@app.route("/")
def index():
    return make_response("Send Request at: /requests/")


@app.route("/request/", methods=["POST"])
def process_request():
    req = request.get_json()
    uid = req["uid"]
    if rate_limit_redis(uid):
        return {"Status": "OK"}
    return {"Status": "Reject"}


if __name__ == "__main__":
    app.run()
