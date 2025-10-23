# zero promttig or short prompt
# few short promtting
# chain of thought

from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()



client = OpenAI()

sytemprompt="""you are a good in maths to calultate only sum and substraction and multiplication and division exept it  you do not know  anything other than math if user ask other things then say sorry i m not able to answer.
To give the output to the user you have to anlyze the question the break it in steps
 follow the squence that is anylyse ,think,output,validate,result

rules:
if user ask any other things then say sorry i m not able to answer and  do not output anything
output the json format as per schema
follow the one step at the time and wait for next input
carefully analyze the question and break it in steps 

example:
if user ask which is not related to sum and substraction and multiplication and division then say sorry i m not able to answer and  do not output anything

output:{"step":"result","content":"Sorry i m not able to answer"},

example:
input:what is 2+2 
output:{"step:anylse","content":"anylying the proble of 2+2},
output:{"step:think","content":" 2+2=4"},
output:{"step:output","content":"sum of 2+2 is 4"},
output:{"step:validate","content":"seems like it is sum of 2+2 is 4 "},
output:{step:result","content":"4"},
}


"""

message = [
    {
        "role": "system",
        "content": sytemprompt,
    },
]

query=input("Enter your query: ")
message.append(
    {
        "role": "user",
        "content": query,
    }
)

while True:
    response = client.chat.completions.create(
    model="gpt-4.1-mini",  # Use a valid model name like "gpt-4o" or "gpt-4"
    response_format={"type": "json_object"},

    messages=message
)



# Print the model's response
    message.append(
        {
            "role": "assistant",
            "content": response.choices[0].message.content,
        
    })
    parsed=json.loads(response.choices[0].message.content)
    # print(parsed)

    if parsed.get("step")!="result":
        print(f"🧠🧠🦕🦕{parsed.get("step")} :- {parsed.get('content')}")

        continue
    else:
        print(f"🤖🤖🤖:- {parsed.get('content')}")
        break



