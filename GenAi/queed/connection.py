# import redis
# from rq import Queue

# redis_conn = redis.Redis(host="localhost", port=6379, db=0)
# print(redis_conn.ping())
# myqueue = Queue("default", connection=redis_conn)
import redis
import json
import uuid

r = redis.Redis(host="localhost", port=6379)

QUEUE_NAME = "task_queue"

def enqueue_job(data: dict):
   job_id = str(uuid.uuid4())
   data["job_id"] = job_id
 
   r.lpush(QUEUE_NAME, json.dumps(data))
   return job_id

def dequeue_job(timeout=5):
    job = r.brpop(QUEUE_NAME, timeout=timeout)  # Wait 5 seconds for a job
   
    if job is None:
        return None  # No job found within 5 sec
    _, data = job
    return json.loads(data)

def store_result(job_id: str, result: str):
    
    r.set(f"result:{job_id}", result,ex=120)
