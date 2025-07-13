import os
from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

def create_tools(ensemble_retriever):
    theme_description = os.getenv("THEME_DESCRIPTION")  
    project_name = os.getenv("PROJECT_NAME")  

    retrieval_tool = create_retriever_tool(
        ensemble_retriever,
        "search_database",
        f"""Searches and retrieves relevant excerpts from a collection of documents on {theme_description}, covering key topics and examples relevant to the theme."""
    )

    @tool
    def web_search_tool(messages: str) -> str:
        """
        Perform a web search using TavilySearchResults to retrieve relevant information.
        """
        search = TavilySearchResults(max_results=3, search_depth="advanced", include_answer=True, include_raw_content=True)
        try:
            search_results = search.invoke(messages)
            results = "\n".join([f"URL: {res['url']}\nContent: {res['content']}\n" for res in search_results])
            return results
        except Exception as e:
            return f"Error performing web search: {e}"

    @tool
    def off_topic_tool(messages: str) -> str:
        """
        Handles off-topic queries unrelated to the specified theme.
        """
        return f"I'm {project_name}; designed by 🅱🅻🅰🆀 to ONLY talk about {theme_description}."

    return [retrieval_tool, web_search_tool, off_topic_tool]