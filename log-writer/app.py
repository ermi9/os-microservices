import redis
import time
from datetime import datetime

REDIS_CHANNEL = "system_stats"

def main():
    r = redis.Redis(host='redis-cache', port=6379)
    pubsub = r.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)

    with open("logs/system_stats.log", "a") as log_file:
        print("Log-writer started, listening for messages...")
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode('utf-8')
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"[{timestamp}] {data}\n"
                log_file.write(log_line)
                log_file.flush() 
                print(log_line, end='')

if __name__ == "__main__":
    main()
