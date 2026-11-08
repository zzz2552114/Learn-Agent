from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv



class AsyncAgent:
    def __init__(self):
        apikey = os.getenv("LLM_API_KEY")
        baseurl = os.getenv("LLM_BASEURL")
        self.model = os.environ["LLM_MODEL_ID"]
        self.client = AsyncOpenAI(api_key=apikey,base_url=baseurl)
    async def think(self,message):
        response = await self.client.responses.create(
            model=self.model,
            instructions=message[0],
            input=message[1],
            stream=False
        )
        return response

async def main():
    load_dotenv()
    Agent = AsyncAgent()
    message = [
        "简要解释一下用户的输入",
        """from openai import OpenAI
client = OpenAI(base_url="https://agi.tongji.edu.cn/v1", api_key="<你的 API Key>")
resp = client.responses.create(model="DeepSeek-V4.1-Flash", input="你好，请介绍一下你自己")
print(resp.output_text)"""
            ]
    try:
        response = await Agent.think(message=message)
        print(f"正文回答:\n\n{response.output_text}\n\n")
        print(f"meta信息：\nid:{response.model}  status:{response.status}  usage:{response.usage}")
    finally:
        await Agent.client.close()

if __name__ == '__main__':
    asyncio.run(main())