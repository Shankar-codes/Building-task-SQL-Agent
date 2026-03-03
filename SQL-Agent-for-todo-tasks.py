# ============================================================================
# SQL Agent for Task Management - Streamlit Application
# ============================================================================
# Purpose: Interactive task management system using LLM agent with SQL database
# Features: Create, Read, Update, Delete tasks with natural language interface
# ============================================================================

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import required libraries for LLM and database operations
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================
# Initialize SQLite database and create tasks table if it doesn't exist
# Table stores task management data with status tracking
db=SQLDatabase.from_uri("sqlite:///my_tasks.db")
db.run("""
       create table if not exists tasks (
           id integer primary key autoincrement,
              title text not null,
              description text,
              status text check(status in ('pending', 'in progress', 'completed')) not null default 'pending',
              created_at timestamp default current_timestamp              
         )
    """)

# ============================================================================
# LLM AND TOOLS SETUP
# ============================================================================
# Initialize Groq LLM model with streaming capability for real-time responses
model = ChatGroq(model="openai/gpt-oss-120b", streaming=True)

# Create toolkit to provide SQL database tools to the agent
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

# ============================================================================
# AGENT SYSTEM PROMPT
# ============================================================================
# Define behavioral rules for the AI agent when executing database operations
# Ensures consistent formatting and safe query execution
system_prompt="""
You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in the browser.

CRUD OPERATIONS:
	CREATE: INSERT INTO tasks(title, description, status)
	READ: SELECT * FROM tasks WHERE ... LIMIT 10
	UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
	DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in progress/completed),created_at.
"""

# ============================================================================
# AGENT CREATION AND CACHING
# ============================================================================
# Cache agent to prevent unnecessary re-initialization on every Streamlit rerun
@st.cache_resource
def get_agent():
    # Create LangChain agent with database tools, LLM model, and system prompt
    agent=create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
        
    )
    return agent

# Initialize agent instance
agent=get_agent()

# ============================================================================
# STREAMLIT UI SETUP
# ============================================================================
# Configure page title and headers for the web interface
st.title("SQL Agent for Task Management")
st.subheader("Task Management Agent using SQL Database and LLM")

# Initialize session state to persist messages across page reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from conversation history
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# ============================================================================
# USER INPUT AND AGENT RESPONSE
# ============================================================================
# Get user input through chat interface
prompt=st.chat_input("Ask me to create, read, update, or delete tasks in the database!")

# Process user query if provided
if prompt:
    # Display user message in chat interface and save to history
    st.chat_message("user").markdown(prompt) 
    st.session_state.messages.append({"role": "user", "content": prompt})  
    
    # Process query with agent and stream response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Invoke agent with user message and persistent thread ID for context
            response=agent.invoke({"messages":[{"role":"user","content":prompt}]},
                                {"configurable": {"thread_id": "1"}}
                                )
            # Extract and display AI response
            result=response["messages"][-1].content
            st.markdown(result)
            # Save assistant response to conversation history
            st.session_state.messages.append({"role": "assistant", "content": result})   
            