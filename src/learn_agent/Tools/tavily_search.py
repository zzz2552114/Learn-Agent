from tavily import TavilyClient
from requests.exceptions import HTTPError
import os
from learn_agent.Tools import Toolregister

@Toolregister
def search(query:str,counts:int = 10) -> str:
    api_key = os.getenv("TAVILY_API_KEY")

    tavily_client = TavilyClient(api_key = api_key)
    param = {
        "query" : query,
        "max_results" : counts,
        "country" : "china",
        "language" : "zh-cn"
    }

    try:
        results = tavily_client.search(**param)
    except HTTPError as e:
        print(f"发生错误：{e}")
        return str(e)
    llm_answer = results.get("answer","LLM didn't generate answer.")
    contents = results.get("results",["no content"])
    res = [
        f"Rank{i}: relevance score: {result.get("score","null")}\ntitle: {result.get("title")}\ncontent: {result.get("content")}"
        for i,result in enumerate(contents)
    ]
    return "\n".join(res)

                


