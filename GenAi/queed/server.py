# from fastapi import FastAPI, Query
# from connection import myqueue
# from worker import process_task

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "server is running"}


# @app.post("/add")
# async def add(query: str = Query(..., description="The search query")):
#    job= myqueue.enqueue(process_task,query)


#    return {"job_id":job.id}

from fastapi import FastAPI, Query
from connection import enqueue_job
from redis import Redis
from fastapi.responses import StreamingResponse
import asyncio
from fastapi.middleware.cors import CORSMiddleware
r = Redis(host="localhost", port=6379, db=0, decode_responses=True)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
async def root():
    return {"message": "server is running"}


@app.post("/add")
async def add(query: str  = Query(..., description="The search query")):
    job = enqueue_job({"query":query})
   
    return job
@app.get("/result/{job_id}")

async def get_result(job_id: str):
    print(job_id)
    async def event_stream():
        while True:
            result = r.get(f"result:{job_id}")
          
            if result is not None:

                yield f"data: {result}\n\n"

                break
            await asyncio.sleep(1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
   