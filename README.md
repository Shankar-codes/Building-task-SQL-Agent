# 🧠 SQL Agent for Task Management (Streamlit + LangChain + Groq)

An AI-powered Task Management system that allows users to Create, Read, Update, and Delete tasks using **natural language**.

Built using:
- LangChain Agent
- Groq LLM
- SQLite Database
- Streamlit UI
- LangGraph Memory

---

## 🚀 Project Overview

This application uses a Large Language Model (LLM) as an intelligent agent that interacts with a SQL database.

Instead of writing SQL queries manually, users can type natural language instructions like:

- "Create a task to finish the report"
- "Show all pending tasks"
- "Mark task 2 as completed"
- "Delete the task called 'Buy groceries'"

The AI agent automatically:
1. Understands user intent
2. Generates safe SQL queries
3. Executes them
4. Returns structured results

---

## 🏗️ Architecture

User (Streamlit Chat UI)
        ↓
LangChain Agent
        ↓
SQL Toolkit
        ↓
SQLite Database (tasks table)
        ↓
Formatted Response

---

## 🗃️ Database Schema

Table: `tasks`

| Column      | Type      | Description |
|------------|----------|------------|
| id         | Integer (PK) | Auto-incremented ID |
| title      | Text     | Task title (required) |
| description| Text     | Optional description |
| status     | Text     | pending / in progress / completed |
| created_at | Timestamp| Auto-generated timestamp |

---

## ✨ Features

- ✅ Natural Language Task Creation
- ✅ Intelligent Task Filtering
- ✅ Update Task Status
- ✅ Delete Tasks
- ✅ Structured Table Output
- ✅ Conversation Memory (Thread-based)
- ✅ SQL Safety Rules
- ✅ Streaming LLM Responses

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**
- **Groq LLM (openai/gpt-oss-120b)**
- **LangGraph Memory**
- **SQLite**
- **Streamlit**

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/sql-agent-task-manager.git
cd sql-agent-task-manager