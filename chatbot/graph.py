import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_count: int

def create_chatbot_graph():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=api_key,
        temperature=0.2,
    )

    def chatbot(state: State):
        return {
            "messages": [llm.invoke(state["messages"])],
            "user_count": state.get("user_count", 0)
        }

    def count_messages(state: State):
        user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
        return {
            "messages": state["messages"],
            "user_count": len(user_messages)
        }

    def should_continue(state: State):
        return "end" if state.get("user_count", 0) >= 5 else "continue"

    def end_conversation(state: State):
        farewell = AIMessage(content="Thanks for chatting! You've hit the 5 message limit. 🛑 Download your summary below!")
        return {
            "messages": state["messages"] + [farewell],
            "user_count": state["user_count"]
        }

    graph = StateGraph(State)
    graph.add_node("counter", count_messages)
    graph.add_node("chatbot", chatbot)
    graph.add_node("end_conversation", end_conversation)

    graph.add_edge(START, "counter")
    graph.add_conditional_edges("counter", should_continue, {
        "continue": "chatbot",
        "end": "end_conversation"
    })
    graph.add_edge("chatbot", END)
    graph.add_edge("end_conversation", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)