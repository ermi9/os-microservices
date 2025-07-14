# 🐳 OS Microservices

This project is a simple system monitoring app made with Docker. It uses Python microservices that talk to each other through Redis.

---

## 🔧 What It Does

- **monitor-service**: Checks CPU, memory, and running processes, then sends that info using Redis.
- **log-writer**: Listens for that info and saves it (like logs).
- **Redis**: Handles the message passing between the two.

---

## ▶️ How to Run It

1. Clone the repo:
   ```bash
   git clone https://github.com/ermi9/os-microservices.git
   cd os-microservices
   
2.
```
docker-compose up --build
```
3. Test the monitor-service:

curl http://localhost:5000/cpu
curl http://localhost:5000/memory
curl http://localhost:5000/pids

