from typing import TypedDict,List,Optional,Annotated
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(BaseModel):
    messages : Annotated[List[BaseMessage],add_messages] = []
    

