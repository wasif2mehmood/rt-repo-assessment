from qwen_chat import LocalQwenChat
from langchain.prompts import ChatPromptTemplate

class RepoAnalyzerAgent:
    def __init__(self):
        self.llm = LocalQwenChat()

    def analyze(self, repo_content):
        prompt = ChatPromptTemplate.from_template(
            "Analyze the following repository content:\n{repo_content}\n\n"
            "Identify key components such as project goals, features, missing sections, etc."
        )
        chain = prompt | self.llm
        return chain.invoke({"repo_content": repo_content})


class MetadataRecommenderAgent:
    def __init__(self):
        self.llm = LocalQwenChat()

    def recommend(self, keywords):
        prompt = ChatPromptTemplate.from_template(
            "Given these keywords: {keywords}, suggest relevant tags, categories, and keywords "
            "for an AI/ML project on GitHub."
        )
        chain = prompt | self.llm
        return chain.invoke({"keywords": ", ".join(keywords)})


class ContentImproverAgent:
    def __init__(self):
        self.llm = LocalQwenChat()

    def improve(self, analysis_report):
        prompt = ChatPromptTemplate.from_template(
            "Improve the clarity and presentation of the following analysis report:\n{analysis}\n\n"
            "Rewrite it in a more professional and readable format suitable for publication."
        )
        chain = prompt | self.llm
        return chain.invoke({"analysis": analysis_report.content})