import os
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.responses import ResponseInputParam
from typing import cast

load_dotenv()

class AgentsLLM:
    # 首先是 meta 元信息
    def __init__(self,model:str|None = None , ApiKey:str|None = None,BaseUrl:str|None = None,timeout : int = 60):
        self.model = model or os.getenv("LLM_MODEL_ID","deepseek-flash")
        apikey = ApiKey or os.getenv("LLM_API_KEY")
        baseUrl = BaseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT",60))

        if not all([self.model,apikey,baseUrl]):
            raise ValueError("Model、APIKEY、BaseUrl 有缺失")

        self.client = OpenAI(api_key=apikey,base_url=baseUrl,timeout=timeout)

    # 然后是调用过程
    def think(self,messages:dict[str,str],temperature:float = 0) -> str|None:
        print(f"正在调用 {self.model} 模型...")
        try:
            response = self.client.responses.create(
                model = self.model,
                input = cast(ResponseInputParam,[
                    {
                        "role" : "user",
                        "content" : messages["user"],
                    }
                ]),
                instructions = messages["system"],
                reasoning = {
                    "effort" : "high"
                },
                temperature = temperature,
                stream=True,
            )

            print("大语言模型响应成功：")

            collected = []
            for event in response:
                if event.type == "response.reasoning_text.delta":
                    print(event.delta,end="",flush = True)
                if event.type == "response.output_text.delta":
                    collected.append(event.delta)
            print()
            return "".join(collected)
        except Exception as e:
            print(f"调用 LLM 时发生错误{e}")
            return None

