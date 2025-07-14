from flask import Flask, jsonify
import psutil
import redis
import json
from threading import Thread
import time

app = Flask(__name__)

REDIS_HOST = 'redis-cache'  
REDIS_PORT = 6379
REDIS_CHANNEL = 'system_stats'

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route('/cpu')
def cpu_usage():
    return jsonify({'cpu_percent': psutil.cpu_percent(interval=1)})

@app.route('/memory')
def memory_usage():
    mem = psutil.virtual_memory()
    return jsonify({
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent
    })

@app.route('/pids')
def pids():
    return jsonify({'pids': psutil.pids()})

def publish_stats():
    while True:
        data = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'used': psutil.virtual_memory().used,
                'percent': psutil.virtual_memory().percent,
            },
            'pids': psutil.pids()
        }
        message = json.dumps(data)
        r.publish(REDIS_CHANNEL, message)
        time.sleep(1)  

if __name__ == '__main__':
    publisher_thread = Thread(target=publish_stats, daemon=True)
    publisher_thread.start()

    app.run(host='0.0.0.0', port=5000)
