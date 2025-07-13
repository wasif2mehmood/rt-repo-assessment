from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, RemoveMessage
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from .state import CustomMessagesState
from .tools import create_tools
import streamlit as st
import os, sys
from dotenv import load_dotenv

load_dotenv()

# Configure console for UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def build_graph(ensemble_retriever):
    tools = create_tools(ensemble_retriever)

    project_name = os.getenv("PROJECT_NAME")  
    theme_description = os.getenv("THEME_DESCRIPTION")  

    # Construct the system message using environment variables
    sys_msg = SystemMessage(content=f"""You are {project_name}, created by 🅱🅻🅰🆀 to answer questions solely about {theme_description}. Respond directly and naturally, as if the knowledge is innate, using only information from the tools provided: `search_database` for historical data, `web_search` for current information, and `off_topic_tool` for queries outside the scope - just return - I'm {project_name}; designed by 🅱🅻🅰🆀 to ONLY talk about {theme_description}. - without modification. Never mention sources, texts, or inconsistencies. Use the conversation summary and recent messages to resolve ambiguous references (e.g., 'it' or 'the two' meaning specific art forms or entities). Internally refine queries with the summary and the last 2-3 messages for clarity before selecting the appropriate tool.""")

    llm = ChatOpenAI(
        model=os.getenv("MAIN_MODEL"),
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        default_headers={
            "X-Title": project_name, 
            "HTTP-Referer": "http://localhost",
            "Content-Type": "application/json"
        },
        verbose=True,
        extra_body={"format": "openai"}
    )
    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: CustomMessagesState) -> dict:
        messages = [sys_msg] + state["messages"]
        summary = state.get("summary", "")

        # Update summary 
        if state["messages"] and (not summary or len(state["messages"]) % 2 == 0):  # Update every 2 messages
            summary_prompt = PromptTemplate(
                template=f"""Create a concise summary of the conversation, focusing on key topics, entities, and specific details (e.g., art forms, locations, or time periods) related to {theme_description} history. Include the most recent entities or subjects discussed (e.g., Ife Art, Benin Art) to aid in resolving ambiguous references. Use the existing summary and recent messages to extend it.
                Existing Summary: {{summary}}
                Recent Messages: {{recent_messages}}""",
                input_variables=["summary", "recent_messages"]
            )
            recent_messages = "\n".join([m.content for m in state["messages"][-3:]])  # Use last 3 messages
            formatted_prompt = summary_prompt.format(summary=summary, recent_messages=recent_messages)
            summary_llm = ChatOpenAI(
                model=os.getenv("SUB_MODEL"),
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                default_headers={
                    "X-Title": project_name,  
                    "HTTP-Referer": "http://localhost",
                    "Content-Type": "application/json"
                },
                verbose=True,
                extra_body={"format": "openai"}
            )
            try:
                new_summary = summary_llm.invoke(formatted_prompt).content
                state_update = {"summary": new_summary}
            except Exception as e:
                st.error(f"Error summarizing conversation: {e}")
                state_update = {"summary": summary}
        else:
            state_update = {"summary": summary}

        # Include summary in the messages for context
        context_messages = messages + [SystemMessage(content=f"Conversation Summary: {summary}")]
        response = llm_with_tools.invoke(context_messages)
        state_update["messages"] = state_update.get("messages", []) + [response]

        # Retain more context 
        if len(state["messages"]) > 10:  # Keep last 10 messages
            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-10]]
            state_update["messages"].extend(delete_messages)

        return state_update

    builder = StateGraph(CustomMessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))  
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
        {"tools": "tools", END: END}
    )
    builder.add_edge("tools", "assistant")
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)