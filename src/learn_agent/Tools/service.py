from ..core.client import AgentsLLM
from .setup import manager
from dotenv import load_dotenv
import json

prompt=[
    {
        "type" : "message",
        "role" : "user",
        "content" : "输入100和200，调用魔法函数，告诉我返回值",
    },
    {
        "type" : "message",
        "role" : "system",
        "content" : "用中文思考并回答"
    }
]
tools = manager.get_tools()
agent = AgentsLLM()
def first():

    return agent.stream(tools=tools,input=prompt)

def middle():
    output = first()
    if output is None : 
        return "failed calling"
    for it in output:
        if it.type == "function_call":
            name = it.name
            param = it.arguments
            result = manager.execute(name=name,param=json.loads(param))
            prompt.append(it) # type: ignore
            res = {
                "type" : "function_call_output",
                "call_id" : it.call_id,
                "output" : json.dumps(result)
            }
            prompt.append(res)
    return prompt

def second():
    prompt = middle()
    agent.stream(tools=tools,input=prompt)
            



if __name__ == '__main__':
    load_dotenv(override=True)
    second()

    
