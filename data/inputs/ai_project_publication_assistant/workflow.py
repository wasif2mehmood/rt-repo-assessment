from langgraph.graph import StateGraph, END, START
from typing import Dict, Any
from tools import git_clone_tool, repo_reader_tool, keyword_extractor_tool
from agents import RepoAnalyzerAgent, MetadataRecommenderAgent, ContentImproverAgent
import os
import shutil

class PublicationAssistantState(Dict):
    repo_url: str
    repo_path: str
    repo_content: str
    keywords: list
    analysis_report: Any
    metadata_suggestions: Any
    final_report: Any
    error: str

def clone_repo(state: PublicationAssistantState):
    print("🔗 Validating and cloning repository...")
    result = git_clone_tool.invoke({"repo_url": state["repo_url"]})

    if result["status"] == "success":
        return {"repo_path": result["repo_path"]}
    else:
        return {"error": result["message"]}


def read_repo(state: PublicationAssistantState):
    print("🔍 Reading repository...")
    result = repo_reader_tool.invoke({"repo_path": state["repo_path"]})
    state["repo_content"] = result.get("repo_content", {})
    return {"repo_content": state["repo_content"]}


def extract_keywords(state: PublicationAssistantState):
    print("🔑 Extracting keywords...")
    content = str(state["repo_content"])
    result = keyword_extractor_tool.invoke(content)
    state["keywords"] = result
    return {"keywords": result}


def analyze_repo(state: PublicationAssistantState):
    print("🧾 Analyzing repository...")
    agent = RepoAnalyzerAgent()
    analysis = agent.analyze(state["repo_content"])
    state["analysis_report"] = analysis
    return {"analysis_report": analysis}


def recommend_metadata(state: PublicationAssistantState):
    print("🏷️ Recommending metadata...")
    agent = MetadataRecommenderAgent()
    suggestions = agent.recommend(state["keywords"])
    state["metadata_suggestions"] = suggestions
    return {"metadata_suggestions": suggestions}


def improve_content(state: PublicationAssistantState):
    print("✍️ Improving content...")
    agent = ContentImproverAgent()
    improved_report = agent.improve(state["analysis_report"])
    state["final_report"] = improved_report
    return {"final_report": improved_report}

def cleanup_repo(state: PublicationAssistantState):
    print("🧹 Cleaning up cloned repository...")
    repo_path = state.get("repo_path")
    if repo_path and os.path.exists(repo_path):
        try:
            shutil.rmtree(repo_path)
            print(f"✅ Successfully deleted: {repo_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete {repo_path}: {str(e)}")
    else:
        print("⚠️ No repository path found or already deleted.")
    return {}

def handle_error(state: PublicationAssistantState):
    print(f"❌ Error occurred: {state.get('error', 'Unknown error')}")
    return {}


def route_after_clone(state: PublicationAssistantState):
    if "error" in state:
        return "error_node"
    else:
        return "read_repo"


# Build Graph
workflow = StateGraph(PublicationAssistantState)

# Add Nodes
workflow.add_node("clone_repo", clone_repo)
workflow.add_node("read_repo", read_repo)
workflow.add_node("extract_keywords", extract_keywords)
workflow.add_node("analyze_repo", analyze_repo)
workflow.add_node("recommend_metadata", recommend_metadata)
workflow.add_node("improve_content", improve_content)
workflow.add_node("cleanup_repo", cleanup_repo)
workflow.add_node("handle_error", handle_error)

# Conditional edge
workflow.add_conditional_edges("clone_repo", route_after_clone, {
    "read_repo": "read_repo",
    "error_node": "handle_error"
})


# Set Entry Point
workflow.set_entry_point("clone_repo")

# Define Edges
workflow.add_edge("read_repo", "extract_keywords")
workflow.add_edge("extract_keywords", "analyze_repo")
workflow.add_edge("analyze_repo", "recommend_metadata")
workflow.add_edge("recommend_metadata", "improve_content")
workflow.add_edge("improve_content", "cleanup_repo")
workflow.add_edge("cleanup_repo", END)
workflow.add_edge("handle_error", END)

# Compile Graph
app = workflow.compile()