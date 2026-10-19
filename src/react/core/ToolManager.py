from typing import Any,Callable


class ToolManager:
    def __init__(self):
        self.tools : dict[str,dict[str,Any]] = {}

    def register(self,tool_name:str,description:str,func:Callable):
        # 用于运行时注册工具
        if self.tools.get(tool_name):
            print(f"已有同名 tool，注册失败，请更改名称后再次注册")
        else:
            self.tools[tool_name] = {"description":description,"func":func}
            print(f"工具 {tool_name} 注册成功！")

    def remove(self,tool_name:str):
        # 用于运行时删除工具
        if self.tools.get(tool_name):
            self.tools.pop(tool_name)
            print(f"工具 {tool_name} 删除成功！")
        else:
            print(f"不包含 {tool_name} 工具，删除失败")

    def load_tools(self):
        from react.Tools import Tools
        for tool in Tools:
            self.register(tool["name"],tool["description"],tool["func"])

    def getTool(self,tool_name:str):
        return self.tools.get(tool_name,{}).get("func")

    def AllTools(self) -> str:
        des = [
            f"- {name} : {tool["description"]}"
            for name,tool in self.tools.items()
        ]
        return "\n".join(des)