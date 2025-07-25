from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage

# Import your LangGraph multi-agent builder
from backend.agents.health_agents import Agents  # Make sure this path is correct

# Initialize LangGraph
graph = Agents()
graph = graph.build_graph()

# Initialize FastAPI app
app = FastAPI()

# CORS middleware for frontend compatibility (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in production (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatRequest(BaseModel):
    message: str

# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    print("✅ Chat endpoint triggered")
    
    user_message = request.message
    state = {"messages": [HumanMessage(content=user_message)]}
    
    output = graph.invoke(
        state,
        config={"configurable": {"thread_id": "thread_id_01"}}
    )
    
    tool_calls = []
    for msg in output["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for call in msg.tool_calls:
                tool_calls.append({
                    "tool": call["name"],
                    "args": call["args"],
                })
    
    return {
        "messages": [
            {"role": "assistant", "content": msg.content} for msg in output["messages"]
        ],
        "tool_calls": tool_calls
    }
