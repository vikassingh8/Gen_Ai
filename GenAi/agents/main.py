from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime
import os

load_dotenv()

client = OpenAI()

# def getTime():
#     return datetime.now().strftime("%I:%M %p")


def command(command):
    return os.system(command)


# systemPrompt="""
# you are smart agent who can answer the  related to time questions , becouse of you can't give the data of real time so for time  i have create the function which can give the data of time
# you have

# rules:
# output must be always in json format
# if user ask time then give output else say sorry i m not able to answer


# example:
# input:what is time right now
# output:{"step":"time","content":"you want to know the time"}
# output:{"step":"getTime", "tool":"getTime" ,"content":"the time right now is "}
# output:{"step":"result","content":"the time right now is 12:00 am"}
# """


systemPrompt = """
you are a smart ai agent whose work is to resolve the users query
you work on start,plan,action,observe mode

available tools are "command" it is accept the command and return the output


rulse:
output must be always in json format 
output should be in steps at the time and wait for next input



example:
input:create a folder named test
output:{"step":"analyse","content":"you wanted to create a folder named test"}
output:{"step":"plan","content":"create a folder named test"}
output:{"step":"think","tool":"command","content":"mkdir test"}
output:{"step":"result","content":"folder created"}

"""


query = input("what is your question : ")

message = [
    {
        "role": "system",
        "content": systemPrompt,
    },
    {"role": "user", "content": query},
]

while True:
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=message,
        # response_format={"type": "json_object"}
    )

    message.append({"role": "user", "content": res.choices[0].message.content})

    paerse = json.loads(res.choices[0].message.content)

    # if paerse.get("step")!="result":
    #         print(paerse.get("content"))
    #         continue
    # else: paerse.get("step")=="getTime" and paerse.get("tool")=="getTime"

    # print(getTime())
    # break

    if paerse.get("step") != "think" and paerse.get("tool") != "command":
        print(paerse.get("step"))
        continue
    else:
        paerse.get("step") == "think" and paerse.get("tool") == "command"
    print(command(paerse.get("content")))

    break
