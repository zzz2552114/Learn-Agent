from serpapi import SerpApiClient
import os
from react.Tools import Toolregister

@Toolregister
def search(query : str) -> str:
    """
    一个基于 SerpApi 的 google 搜索引擎工具。
    它会解析搜索结果，返回答案或者知识图谱信息。
    """
    print(f"正在调用 serpapi ")
    api_key = os.getenv("SERP_API_KEY")
    param = {
        "api_key" : api_key,
        "engine" : "google",
        "q" : query,
        "hl" : "zh-cn",
        "gl" : "cn",
        "google_domain" : "google.com",
        "safe" : "off"
    }

    serp_client = SerpApiClient(param)
    results = serp_client.get_dict()

    if "answer_box_list" in results:
        return "\n".join(results["answer_box_list"])
    
    if "answer_box" in results and "answer" in results["answer_box"]:
        return results["answer_box"]["answer"]
    
    if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
        return results["knowledge_graph"]["description"]
    
    if "organic_results" in results and results["organic_results"]:
        snippets = [
            f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
            for i, res in enumerate(results["organic_results"][:3])
        ]
        return "\n\n".join(snippets)
    
    return f"对不起，没有找到关于 '{query}' 的信息。"