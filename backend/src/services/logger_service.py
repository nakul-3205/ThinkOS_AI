import json
import time
import socket
from loguru import logger
from src.clients.redis_client import get_redis

redis = get_redis()

def _push_to_redis(json_log):
    key = "logs:" + time.strftime('%Y-%m-%d')

    try:
        redis.lpush(key, json.dumps(json_log))
    except Exception as e:
        print("Redis push failed:", e)


def serialize_log(record):
    return {
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "level": record["level"].name,
        "message": record["message"],
        "function": record["function"],
        "module": record["module"],
        "file": record["file"].name,
        "line": record["line"],
        "hostname": socket.gethostname(),
    }


def log_sink(message):
    record = message.record
    json_log = serialize_log(record)
    _push_to_redis(json_log)



logger.remove()
logger.add(log_sink)
app_logger = logger