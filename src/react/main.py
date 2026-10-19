from react.core.ReAct import ReActAgent
from react.core.client import AgentsLLM
from react.core.ToolManager import ToolManager


if __name__ == "__main__":
    client = AgentsLLM()
    toolmanager = ToolManager()
    toolmanager.load_tools()
    Agent = ReActAgent(client=client,toolmanager=toolmanager,max_loops=8)
    Agent.run("首先告诉我你是什么模型，然后详细给我说一下近2届足球世界杯金靴得主和金靴前三名")
