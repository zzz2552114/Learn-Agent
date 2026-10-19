from typing import Any
Tools : list[dict[str,Any]] = []

def Toolregister(func):
    name = func.__module__.rsplit('.',1)[-1]
    description = func.__doc__ or "No description"
    Tools.append({
        "type" : "function",
        "name" : name,
        "description" : description,
        "parameters" : {
            "type" : "object",
            "properties" : {
                "query" : {
                    "type" : "string",
                    "description" : "需要联网搜索的问题，或者你需要获取到信息。"
                },
                "counts" : {
                    "type" : "int",
                    "description" : "希望获得的搜索结果的数量"
                },
            },
            "required" : ["query","counts"],
        }
    })
    return func

from . import serp_search
from . import tavily_search
