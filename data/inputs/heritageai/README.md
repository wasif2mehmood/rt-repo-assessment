# **Heritage: AI-Powered Query System for Nigerian Arts & Culture**
![heritage2](https://github.com/user-attachments/assets/111eb4e9-e4a4-47ae-a68f-b004d3a4d5d4)


![CHINONSO ODIAKA's Video - Jun 7, 2025-VEED](https://github.com/user-attachments/assets/642e38a9-4add-45cb-bda1-6807ee6b3d23)


  



### **About the Creator**
Hi! I'm [🅱🅻🅰🆀](https://www.linkedin.com/in/chinonsoodiaka/), an aspiring AI developer passionate about leveraging technology to preserve cultural heritage. Explore my additional projects on my [Github repositories](https://github.com/Blaqadonis)

### **Project Overview**
Welcome to Heritage, an advanced AI-driven chatbot application crafted to celebrate and explore the rich tapestry of Nigerian arts, culture, and pre-historic heritage. Developed by 🅱🅻🅰🆀 as my submission for Week 1 of the [Agentic AI Developer Certification Program 2025](https://app.readytensor.ai/publications/4n07ViGCey0l).
This project showcases an agentic Retrieval-Augmented Generation (RAG) system built with LangGraph. Heritage integrates state-of-the-art (SOTA) language models with tool-calling capabilities, enhanced by real-time web access via Tavily, to deliver a dynamic and insightful chatbot experience. Tailored for deep exploration of Nigerian arts, traditions, and history, the system features a modular, customizable architecture, making it adaptable to various domains.

#### **Key Highlights**
* Advanced Model Integration: Utilizes SOTA models with tool-calling abilities, accessed via OpenRouter for cost efficiency, though Heritage is not a free service due to API costs.
* Modular Design: The system’s theme (currently focused on Nigerian heritage) can be adapted to domains like "Space" or "History" with a compatible knowledge base, thanks to its flexible components.
* Interactive Experience: Offers users an engaging interface for natural language queries, delivering detailed, culturally enriched responses.

### **Introduction**
#### **Purpose**
The primary goal of Heritage is to create an immersive AI query system that educates and engages users—ranging from Nigerian culture enthusiasts to a global audience—about the nation’s rich heritage. It aims to foster cultural appreciation through interactive exploration of art styles, traditions, and historical significance.

### **Features**
#### **Natural Language Query Handling**: 
Ask about Nigerian history, ethnic groups, art forms (e.g., Igbo-Ukwu bronzes, Yoruba Gele), or cultural practices, and receive accurate, context-aware responses.
#### **Real-Time Web Integration**:
Powered by Tavily, Heritage fetches the latest information to complement its knowledge base.
#### **Modular Architecture**:
Swap out components (e.g., data sources or themes) without altering the core structure, enabling easy customization.

### **Getting Started**
#### Prerequisites
* Python 3.10+
* Git (for cloning the repository)
  
API keys for:
* OpenRouter (for LLM access)
* Tavily (for web search)
  
Required libraries (listed in ```requirements.txt```)
#### Installation
1. Clone the Repository:
```
git clone https://github.com/Blaqadonis/heritageai.git
cd heritageai
```
2. Set Up Environment Variables:
Create a ```.env``` file in the root directory with the following:
```
OPENROUTER_API_KEY=your_openrouter_api_key
HF_TOKEN=your_huggingface_api_key
TAVILY_API_KEY=your_tavily_api_key
MAIN_MODEL=meta-llama/llama-4-scout
SUB_MODEL=openai/gpt-4.1-nano
EMBEDDINGS=sentence-transformers/all-mpnet-base-v2
RESET_DB=false
SHOW_SPINNER=true
CHROMA_DB_PATH=./chroma_db
DATA_PATH=./data/
LOGO_PATH=./images/heritage2.png
PROJECT_NAME=Heritage AI
THEME_DESCRIPTION=Nigerian Peoples, Arts, and Culture
FUN_FACTS_FILE=./fun_facts.json
```
3. Install Dependencies:
```
pip install -r requirements.txt
```
4. Run the Application:
```
streamlit run app.py
```

Access the app in your browser at ```http://localhost:8501```.


### **Contributing**
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with your changes. For major updates, open an issue to discuss first.

### **License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms.

### **Acknowledgments**
Thanks to [Ready Tensor](https://app.readytensor.ai/hubs/ready_tensor_certifications) (the organisers of the program) for this opportunity.
Gratitude to the open-source community for tools like LangGraph, Tavily, and Streamlit.

Here is a [link](https://app.readytensor.ai/publications/heritage-an-ai-query-system-for-the-nigerian-peoples-their-pre-historic-arts-cultures-4fBZ6PYkO2mZ) to the publication of this project.

