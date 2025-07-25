from backend.utils.config import *
from backend.models.state import AgentState
from backend.utils.prompts import sys_prompt
from backend.tools.workout import fitness_data_tool
from backend.tools.diet import diet_tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os 
from langchain_core.messages import SystemMessage
from langgraph.graph import END,START,StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

tools = [fitness_data_tool,diet_tool]

class Agents:
    def __init__(self):
        self.prompts = sys_prompt
        self.tools = [fitness_data_tool,diet_tool]
        self.llm = ChatGroq(model=LLM_MODEL,temperature=TEMPERATURE,api_key=GROQ_API_KEY)
        self.memory = MemorySaver()
        
    def assistant_node(self,state:AgentState):
       response = self.llm.invoke([SystemMessage(content=sys_prompt)]+
                          state.messages)
       
       state.messages += [response]
       return state
   
    def assistant_router(self,state:AgentState):
        last_message = state.messages[-1]
        if not last_message.tool_calls:
            return END
        else:
            return "tools"
        
    def build_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node("assistant_node",self.assistant_node) 
        builder.add_node("assistant_router",self.assistant_router) 
        builder.add_node("tools",ToolNode(tools))
        
        builder.add_edge(START,"assistant_node")
        builder.add_conditional_edges("assistant_node",self.assistant_router,["tools",END])
        builder.add_edge("tools","assistant_router")
        
        return builder.compile(checkpointer=self.memory)
    
           