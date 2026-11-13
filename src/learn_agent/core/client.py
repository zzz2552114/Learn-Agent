import os
from openai import OpenAI
from dotenv import load_dotenv




class AgentsLLM:
    # 首先是 meta 元信息
    def __init__(self,model:str|None = None , ApiKey:str|None = None,BaseUrl:str|None = None,timeout : int = 60):
        self.model = model or os.getenv("LLM_MODEL_ID","deepseek-flash")
        apikey = ApiKey or os.getenv("LLM_API_KEY")
        baseUrl = BaseUrl or os.getenv("LLM_BASEURL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT",60))

        if not all([self.model,apikey,baseUrl]):
            raise ValueError("Model、APIKEY、BaseUrl 有缺失")

        self.client = OpenAI(api_key=apikey,base_url=baseUrl,timeout=timeout)

    # 然后是调用过程
    def stream(self,tools,input,temperature:float = 0):
        print(f"正在调用 {self.model} 模型...")
        try:
            response = self.client.responses.create(
                model = self.model,
                input = input,
                reasoning = {
                    "effort" : "high"
                },
                tools=tools,
                temperature = temperature,
                max_output_tokens=30000,
                stream=True
            )
            

            for event in response:
                if event.type == "response.created":
                    print("大语言模型响应成功：")
                    print("\n\n推理：\n\n")
                elif event.type == "response.reasoning_text.delta":
                    print(event.delta,end="")
                elif event.type == "response.reasoning_text.done":
                    print("\n\n正文输出\n\n")
                elif event.type == "response.output_text.delta":
                    print(event.delta,end="")
                elif event.type == "response.output_text.done":
                    print("\n\n\n用量")
                elif event.type == "response.completed":
                    info = event.response
                    model = info.model
                    usage = info.usage
                    print(f"模型: {model}")
                    if usage:
                        print(f"输出: {usage.output_tokens} token, (含推理 {usage.output_tokens_details.reasoning_tokens} token)")
                        print(f"输入: {usage.input_tokens} token")
                        print("\n\n")
                    return event.response.output
                


        except Exception as e:
            print(f"调用 LLM 时发生错误{e}")
            return None

