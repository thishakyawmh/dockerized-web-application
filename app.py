import os

import redis
from flask import Flask, jsonify

app = Flask(__name__)

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


@app.get("/")
def index():
    visits = client.incr("page_visits")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dockerized Web Application</title>
</head>
<body>
  <h1>Dockerized Web Application</h1>
  <p>This Flask app is running in a Docker container.</p>
  <p>Redis has counted <strong>{visits}</strong> page visits.</p>
  <p><a href="/health">Check app health</a></p>
</body>
</html>
"""


@app.get("/health")
def health():
    try:
        client.ping()
    except redis.RedisError:
        return jsonify(status="unhealthy", redis="unavailable"), 503

    return jsonify(status="healthy", redis="connected"), 200
