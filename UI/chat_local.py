from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
import datetime
from backend.agents.health_agents import Agents

graph = Agents()
graph = graph.build_graph()

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# 🧩 Emoji helper
def get_message_emoji(msg):
    if isinstance(msg, HumanMessage):
        return "🧑"
    elif isinstance(msg, AIMessage):
        return "🤖"
    elif isinstance(msg, ToolMessage):
        return "🛠️"
    else:
        return "💬"

# 🧠 Main run loop
def main():
    print(f"{Colors.BOLD}🤖 Welcome to the Multi-Agent Health Assistant! Type 'exit' to quit.{Colors.END}\n")

    while True:
        user_input = input(f"{Colors.OKBLUE}🧑 You: {Colors.END}")
        if user_input.strip().lower() == "exit":
            print(f"{Colors.OKGREEN}👋 Exiting... Stay healthy!{Colors.END}")
            break

        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }

        try:
            output = graph.invoke(
                initial_state,
                config={"configurable": {"thread_id": "id_1"}}
            )

            print(f"\n{Colors.BOLD}📡 Assistant Response at {datetime.datetime.now().strftime('%H:%M:%S')}{Colors.END}\n")

            for msg in output["messages"]:
                emoji = get_message_emoji(msg)

                if isinstance(msg, HumanMessage):
                    print(f"{emoji} {Colors.OKBLUE}User: {msg.content}{Colors.END}")
                elif isinstance(msg, AIMessage):
                    print(f"{emoji} {Colors.OKCYAN}Assistant: {msg.content}{Colors.END}")
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tool_name = tool_call.get("name", "Unknown Tool")
                            tool_args = tool_call.get("args", {})
                            print(f"   🔧 {Colors.OKGREEN}Tool Called: {tool_name}{Colors.END}")
                            print(f"   📤 Arguments  : {tool_args}")
                elif isinstance(msg, ToolMessage):
                    print(f"{emoji} {Colors.OKGREEN}Tool Output: {msg.content}{Colors.END}")
                else:
                    print(f"{emoji} {Colors.WARNING}Unknown Message Type: {msg.content}{Colors.END}")

            print(f"{Colors.OKBLUE}" + "─" * 60 + f"{Colors.END}\n")

        except Exception as e:
            print(f"{Colors.FAIL}❌ Error occurred: {e}{Colors.END}\n")


if __name__ == "__main__":
    main()