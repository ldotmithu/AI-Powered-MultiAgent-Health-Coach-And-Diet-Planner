# 🏋️ AI Health & Fitness Assistant

Welcome to the **AI Health & Fitness Assistant** — a smart, multi-agent AI-powered app that helps you achieve your fitness and nutrition goals with personalized workout routines and meal plans!

---

## 🚀 Project Overview

This application combines:

- **LangGraph Multi-Agent System**: Orchestrates fitness and diet tools powered by OpenAI-style LLMs.
- **FastAPI Backend**: Serves the AI assistant API for chat requests.
- **Streamlit Frontend**: An interactive and visually appealing chat UI for users.
- **Third-Party APIs**:
  - Fitness exercises from [API Ninjas](https://api-ninjas.com/api/exercises)
  - Meal and recipe plans from [Spoonacular](https://spoonacular.com/food-api)

---

## 🎯 Key Features

- Personalized workout plan recommendations by muscle groups & difficulty
- Customized diet plans (vegan, vegetarian, general) with detailed recipes
- Conversational AI assistant with natural language understanding
- Tool call tracking displayed live in the UI sidebar for transparency & debugging
- Responsive and user-friendly chat interface with message history
- Easy integration via REST API (`/chat` endpoint)

---

## 💻 Tech Stack

| Layer           | Technology                |
|-----------------|---------------------------|
| AI & Agents     | LangGraph, LangChain, ChatGroq LLM |
| Backend API     | FastAPI                   |
| Frontend UI     | Streamlit                 |
| APIs           | API Ninjas, Spoonacular    |
| Environment     | Python 3.10+, dotenv       |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- API keys for:
  - API Ninjas (Fitness): `EXERCISE_API_KEY`
  - Spoonacular (Diet): `DIET_API_KEY`
- Your LangGraph + LLM API key (e.g. Groq or OpenAI)

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/ai-health-fitness-assistant.git
cd ai-health-fitness-assistant
```

### 2. Create & Activate Virtual Environment
```
python -m venv venv
venv\Scripts\activate 
```

### 3. Install Dependencies
```
pip install -r requirements.txt

```

### 4. Setup Environment Variables
```
EXERCISE_API_KEY=your_api_ninjas_key_here
DIET_API_KEY=your_spoonacular_key_here
GROQ_API_KEY=your_langchain_or_groq_key_here

```
### 5. Run the Backend FastAPI Server
```
uvicorn backend.main:app --reload
```
### 6. Run the Streamlit Frontend
```
streamlit run UI\app.py
```
- Open your browser at http://localhost:8501 and start chatting with your AI assistant!
