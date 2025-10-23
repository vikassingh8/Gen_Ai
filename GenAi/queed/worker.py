import time
from connection import dequeue_job, store_result
from chat import chat as testchat

print("🚀 Worker started. Waiting for jobs...")
while True:
    job = dequeue_job()
  
    if job is None:
        print("No more jobs to process. Sleeping...")
        time.sleep(2)
        continue

    try:
        res = testchat(job["query"])
        id = job["job_id"]

        # print(f"🧠 Chat Response:\n{res}\n\n {id}")
        store_result(id, res)


    except Exception as e:
        print(f"❌ Error: {e}")

    time.sleep(1)
