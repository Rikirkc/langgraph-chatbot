# 🤖 LangGraph Chatbot (with Gemini & Streamlit)

This is a simple chatbot app built using **LangGraph**, **LangChain**, **Google Gemini (gemini-2.0-flash)**, and **Streamlit**. It demonstrates how to:

* Use LangGraph to build a stateful chatbot
* Integrate Google Gemini as the LLM
* Add a message counter to end chat after 5 user messages
* Store memory using LangGraph's built-in memory system
* Generate a PDF summary of the conversation

---

## 📁 Project Structure

```
├── app.py                      # Streamlit UI and chat logic
├── .env                        # Stores GEMINI_API_KEY
├── requirements.txt            # Python dependencies
└── chatbot/
    ├── __init__.py
    ├── graph.py                # LangGraph chatbot logic and flow
    └── pdf_generator.py        # PDF summary generation
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Rikirkc/langgraph-chatbot.git
cd langgraph-gemini-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_api_key_here
```

### 4. Run the chatbot

```bash
streamlit run app.py
```

---

## 💡 How It Works

### 🌐 `graph.py`

* Defines a LangGraph with three key nodes:

  * `counter`: tracks number of user messages
  * `chatbot`: generates responses using Gemini
  * `end_conversation`: gracefully ends chat after 5 user messages
* Uses `MemorySaver` for LangGraph memory (stores state)

### 🧠 `gemini-1.5-flash`

* Fast, efficient model by Google Gemini
* Used via LangChain’s `ChatGoogleGenerativeAI` class

### 🧾 `pdf_generator.py`

* Uses ReportLab to generate a styled PDF report with all messages
* Available for download after conversation ends

### 🖥️ `app.py`

* Streamlit UI:

  * Sidebar with status and reset button
  * Chat UI for messages
  * Auto ends conversation after 5 messages
  * Option to download a PDF summary

---

## 📦 Requirements

```text
streamlit
langgraph
langchain
langchain-google-genai
python-dotenv
reportlab
typing_extensions
```

Install via:

```bash
pip install -r requirements.txt
```

---

## 🧪 Example Prompts

* "Tell me a fun fact about space."
* "What is LangGraph used for?"
* "Summarize the concept of vector databases."

Try sending 5 messages — the chatbot will auto-terminate afterward.

---

## 🧠 Why This Project?

This app is perfect for showcasing:

* LangGraph state machine logic
* Working memory integration
* Real-world Streamlit UX
* Gemini model usage in production
* PDF document generation pipelines

---

## 🛠️ Future Ideas

* Add tool calling (Gemini Pro)
* Store chats in a database
* Multi-session support
* Better PDF styling with emojis or markdown

---
