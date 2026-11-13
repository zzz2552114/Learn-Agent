from dataclasses import dataclass
from pydantic import BaseModel,ValidationError
from typing import Callable

@dataclass
class ToolSpec:
    name : str
    description : str
    parameters : type[BaseModel]
    handler : Callable
    read_only : bool


class ToolManager:
    def __init__(self):
        self.tools : dict[str,ToolSpec]= {}

    def get_tools(self):
        to_tools = []
        for tool in self.tools.values():
            to_tool = {
                "type" : "function",
                "name" : tool.name,
                "description" : tool.description,
                "parameters" : tool.parameters.model_json_schema(),
                "strict" : False,
            }
            to_tools.append(to_tool)
        return to_tools

    
    def register(self,tool : ToolSpec):
        if tool.name in self.tools:
            raise ValueError(f"Tool already registered : {tool!r}")
        self.tools[tool.name] = tool

    def execute(self,name,param):
        if name not in self.tools : 
            raise ValueError(f"{name} tool not found")
        tool = self.tools[name]
        try:
            args = tool.parameters.model_validate(param,strict=False)
        except ValidationError as e:
            return {"error": "invalid_arguments",
                    "details": e.errors(include_url=False)}
        res = tool.handler(**args.model_dump())
        return res  