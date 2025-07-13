import streamlit as st
import plotly.express as px
import requests
import os
from datetime import datetime
import time
import random, sys
import json
from uuid import uuid4
from langchain_core.messages import HumanMessage, AIMessage
from src.graph import build_graph
from vectorstore import load_db
from dotenv import load_dotenv

load_dotenv()

# Configure console for UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_name = os.getenv("PROJECT_NAME", "Heritage AI")
theme_description = os.getenv("THEME_DESCRIPTION")
fun_facts_file = os.getenv("FUN_FACTS_FILE")
logo_path = os.getenv("LOGO_PATH")
welcome_message = os.getenv("WELCOME_MESSAGE", f"Welcome to {project_name}!")

# Load fun facts from a file
try:
    with open(fun_facts_file, "r") as f:
        FUN_FACTS = json.load(f)
except FileNotFoundError:
    print("No FUN_FACTS file provided.")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #4A0000;
        color: #FFFFFF;
    }
    .main {
        font-family: 'Ubuntu', sans-serif;
        background-color: #4A0000;
    }
    .chat-message-user {
        background-color: #000000;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border: 2px solid #8B0000;
    }
    .chat-message-ai {
        background-color: #2F1B1B;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border: 2px solid #000000;
    }
    .sidebar .sidebar-content {
        background-color: #2F1B1B;
        color: #FFFFFF;
        border-right: 5px solid #000000;
    }
    a {
        color: #FF4500;
        text-decoration: underline;
    }
    a:hover {
        color: #FFFFFF;
    }
    .proudly-nigerian {
        font-size: 12px;
        line-height: 1;
        color: #FFD700;
    }
    .stTextInput > div > div > input {
        background-color: #2F1B1B;
        border: 2px solid #000000;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: 2px solid #8B0000;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #8B0000;
        color: #FFFFFF;
        border: 2px solid #000000;
    }
    .stTable table {
        background-color: #4A0000;
        color: #FFFFFF;
        border-collapse: collapse;
    }
    .stTable th {
        background-color: #000000;
        color: #FFFFFF;
        padding: 10px;
        border: 2px solid #8B0000;
    }
    .stTable td {
        padding: 10px;
        border: 2px solid #000000;
    }
    .css-1aumxhk {
        background-color: #000000;
        color: #FFFFFF;
        border: 2px solid #8B0000;
    }
    .thinking-message {
        font-style: italic;
        color: #FFD700;
    }
    /* Ensure spinner and text are visible */
    .stSpinner > div {
        background-color: #2F1B1B !important;
        border-top: 4px solid #FFD700 !important;
        border-right: 4px solid #FF4500 !important;
        border-bottom: 4px solid #00CED1 !important;
        border-left: 4px solid #8B0000 !important;
    }
    .stSpinner::before {
        content: attr(data-message);
        color: #FFD700;
        font-weight: bold;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Initialize vector store and retriever
    if "vector_store" not in st.session_state or "ensemble_retriever" not in st.session_state:
        reset_db = os.getenv("RESET_DB", "False").lower() == "true"
        vector_store, ensemble_retriever = load_db(reset=reset_db)
        st.session_state.vector_store = vector_store
        st.session_state.ensemble_retriever = ensemble_retriever
    else:
        vector_store = st.session_state.vector_store
        ensemble_retriever = st.session_state.ensemble_retriever

    app = build_graph(ensemble_retriever)
    config = {"configurable": {"thread_id": str(uuid4())}}

    # Streamlit app
    st.title(project_name)

    # Set dynamic login time
    if "login_time" not in st.session_state:
        st.session_state.login_time = datetime.now().strftime('%I:%M %p WAT on %A, %B %d, %Y')
    st.markdown(f"**{welcome_message} You logged in at {st.session_state.login_time}.**")

    # Sidebar
    with st.sidebar:
        page_options = ["Landing", "About", "Chat", "Statistics"]
        display_names = ["Home", "About", "Chat", "Statistics"]
        current_index = page_options.index(st.session_state.get("page", "Landing"))
        selected_page = st.selectbox(
            "Choose a page",
            options=page_options,
            index=current_index,
            format_func=lambda x: display_names[page_options.index(x)]
        )
        if selected_page != st.session_state.get("page"):
            st.session_state.page = selected_page
            st.rerun()
        st.markdown("### Cultural Nuggets")
        if "last_fact_time" not in st.session_state:
            st.session_state.last_fact_time = time.time()
            st.session_state.current_fact = random.choice(FUN_FACTS)
        current_time = time.time()
        if current_time - st.session_state.last_fact_time >= 60:
            st.session_state.current_fact = random.choice(FUN_FACTS)
            st.session_state.last_fact_time = current_time
        fact_placeholder = st.empty()
        with fact_placeholder.container():
            st.markdown(f"**Did you know?** {st.session_state.current_fact['text']}")
            try:
                response = requests.get(st.session_state.current_fact["image"])
                if response.status_code == 200:
                    st.image(st.session_state.current_fact["image"], width=100)
            except Exception:
                pass

    # Session state
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if "last_datasource" not in st.session_state:
        st.session_state.last_datasource = "off_topic"
    if "page" not in st.session_state:
        st.session_state.page = "Landing"
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Update page
    page = st.session_state.page

    # Landing Page
    if page == "Landing":
        st.header(f"Welcome to an AI query system for {theme_description}.")
        st.write(f"""
            Discover the rich heritage with {project_name}! This app is designed to educate and engage 
            users about {theme_description} through an interactive query-answer system and insightful statistics. Explore 
            the history, traditions, and expressions of diverse communities.
        """)
        # Check if logo_path is valid before displaying
        if logo_path and (os.path.exists(logo_path) or logo_path.startswith(('http://', 'https://'))):
            st.image(logo_path, width=300, caption=project_name)
        else:
            st.warning("Logo image not found. Please set a valid LOGO_PATH in .env.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Flag_of_Nigeria.svg/120px-Flag_of_Nigeria.svg.png", width=50)
        st.markdown('<p class="proudly-nigerian">Proudly Nigerian</p>', unsafe_allow_html=True)
        if st.button("Get Started"):
            st.session_state.page = "Chat"
            st.rerun()

    # About Page
    if page == "About":
        st.header(f"About {project_name}")
        st.write(f"""
            {project_name} is a passion project created to celebrate {theme_description}. It leverages advanced AI to provide 
            insights into the arts, cultures, and peoples of Nigeria. This app was designed and developed by [🅱🅻🅰🆀](https://www.linkedin.com/chinonsoodiaka), 
            a dedicated enthusiast of Nigerian culture.

            This project is also the submission for the **AAIDC Module 1 Project: Foundations of Agentic AI – Your First RAG Assistant**. 
            You can watch the project walkthrough and demonstration here: [AAIDC Module 1 Project](https://youtu.be/mkyc5AZxtXU).
        """)
        st.write("Feel free to connect with the author on LinkedIn for more information or collaboration opportunities!")

    # Chat Page
    if page == "Chat":
        for entry in st.session_state.query_history:
            st.markdown(f"<div class='chat-message-user'>You: {entry['query']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-message-ai'>{project_name}: {entry['response']}</div>", unsafe_allow_html=True)
        user_input = st.chat_input(f"Ask about {theme_description}:")
        if user_input:
            st.markdown(f"<div class='chat-message-user'>You: {user_input}</div>", unsafe_allow_html=True)
            st.session_state.chat_messages.append(HumanMessage(content=user_input))
            state = {"messages": st.session_state.chat_messages, "summary": st.session_state.summary}
            st.session_state.searching = True
            
            # Single invocation with uniform spinner
            show_spinner = os.getenv("SHOW_SPINNER", "true").lower() == "true"
            if show_spinner:
                with st.spinner("Responding..."):
                    result = app.invoke(state, config)
            else:
                status_placeholder = st.empty()
                status_placeholder.markdown("<div class='thinking-message'>Thinking...</div>", unsafe_allow_html=True)
                result = app.invoke(state, config)
            
            response = "I don’t know."
            datasource = result.get("last_datasource", "off_topic")
            documents = result.get("documents", [])
            for msg in reversed(result['messages']):
                if isinstance(msg, AIMessage):
                    if msg.content in ["search_database", "web_search", "off_topic"]:
                        datasource = msg.content
                    elif not msg.content.startswith("Route to"):
                        response = msg.content
                        break
            st.session_state.last_datasource = datasource
            st.session_state.summary = result.get("summary", st.session_state.summary)
            st.session_state.chat_messages.append(AIMessage(content=response))
            
            if 'status_placeholder' in locals():
                status_placeholder.empty()
            st.markdown(f"<div class='chat-message-ai'>{project_name}: {response}</div>", unsafe_allow_html=True)
            st.session_state.query_history.append({
                "query": user_input,
                "response": response,
                "datasource": datasource,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "documents": documents
            })
            st.session_state.searching = False

    # Statistics Page
    if page == "Statistics":
        st.markdown(f"### {project_name} Insights")
        if not st.session_state.query_history:
            st.write("No queries yet. Start chatting to see stats!")
        else:
            st.subheader("Query Metrics")
            datasource_counts = {"Web Search": 0, "Database": 0, "Off-Topic": 0}
            for entry in st.session_state.query_history:
                if entry["datasource"] == "web_search":
                    datasource_counts["Web Search"] += 1
                elif entry["datasource"] == "search_database":
                    datasource_counts["Database"] += 1
                else:
                    datasource_counts["Off-Topic"] += 1
            total_queries = len(st.session_state.query_history)
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total Queries", total_queries)
            with col2: st.metric("Web Searches", datasource_counts["Web Search"])
            with col3: st.metric("Database Searches", datasource_counts["Database"])
            with col4: st.metric("Off-Topic Queries", datasource_counts["Off-Topic"])
            st.subheader("Query Topics Distribution")
            topic_counts = {"Art": 0, "Culture": 0, "Other": 0}
            for entry in st.session_state.query_history:
                query_lower = entry["query"].lower()
                if "art" in query_lower: topic_counts["Art"] += 1
                elif "culture" in query_lower: topic_counts["Culture"] += 1
                else: topic_counts["Other"] += 1
            total_topic_queries = sum(topic_counts.values())
            if total_topic_queries > 0:
                fig_pie = px.pie(
                    values=list(topic_counts.values()),
                    names=list(topic_counts.keys()),
                    color_discrete_sequence=["#FF4500", "#00CED1", "#FFD700"],
                    labels={"value": "Count", "label": "Topic"}
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(size=12, color='#000000'))
                st.plotly_chart(fig_pie)
            else:
                st.write("No topic data to display yet. Try making some queries!")
            
            st.subheader("Query Topics")
            topic_counts = {"Art": 0, "Culture": 0, "Other": 0}
            for entry in st.session_state.query_history:
                query_lower = entry["query"].lower()
                if "art" in query_lower: topic_counts["Art"] += 1
                elif "culture" in query_lower: topic_counts["Culture"] += 1
                else: topic_counts["Other"] += 1
            total_topic_queries = sum(topic_counts.values())
            if total_topic_queries > 0:
                fig_bar = px.bar(
                    x=list(topic_counts.keys()),
                    y=list(topic_counts.values()),
                    labels={"x": "Topic", "y": "Number of Queries"},
                    color_discrete_sequence=["#8B0000"]
                )
                st.plotly_chart(fig_bar)
            else:
                st.write("No topic data to display yet. Try asking about art or culture!")
            st.subheader("Query History")
            query_data = []
            for entry in st.session_state.query_history:
                docs = entry["documents"]
                doc_titles = [doc.page_content[:50] + "..." if len(doc.page_content) > 50 else doc.page_content for doc in docs] if docs else ["No documents"]
                query_data.append({
                    "Query": entry["query"],
                    "Response": entry["response"],
                    "Datasource": "Web Search" if entry["datasource"] == "web_search" else "Database" if entry["datasource"] == "search_database" else "Off-Topic",
                    "Timestamp": entry["timestamp"],
                    "Documents": ", ".join(doc_titles)
                })
            st.table(query_data)

if __name__ == "__main__":
    main()