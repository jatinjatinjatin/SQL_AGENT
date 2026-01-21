🧠 SQL Agent – AI-Powered Natural Language to SQL Dashboard

SQL Agent is an AI-powered data analysis platform that converts natural language questions into secure, optimized SQL queries using Ollama (LLaMA 3). It executes queries on SQLite databases and visualizes results through an interactive Streamlit dashboard.

No API keys. No cloud dependency. Fully local. ⚡

✨ Features

🧠 Natural language → SQL using LLaMA 3 (Ollama)

🔐 Read-only SQL enforcement (blocks DELETE, DROP, UPDATE, etc.)

🧹 Automatic SQL repair & syntax correction

📊 Interactive dashboard (Bar, Line, Area, Pie, Auto)

📁 CSV upload → auto-create database tables

📤 Export results to CSV

🕒 Query history

📌 Saved dashboards

⚙️ Query optimizer & LIMIT injection

🗄 SQLite backend

⚡ FastAPI backend API

🏗 Architecture
frontend/   → Streamlit dashboard
backend/    → FastAPI + SQLite + Ollama
app.db      → Database

🚀 Getting Started
1️⃣ Install Requirements
pip install fastapi uvicorn streamlit pandas matplotlib requests


Install Ollama:

👉 https://ollama.com

Pull the model:

ollama pull llama3

2️⃣ Start Backend
cd backend
uvicorn main:app --reload


Runs at:

http://127.0.0.1:8000

3️⃣ Start Frontend
cd frontend
streamlit run app.py


Open browser:

http://localhost:8501

🧪 Example Questions to Try

Total transactions per city

Percentage of failed transactions

Average transaction amount by status

📂 CSV Upload

Upload any CSV file from the sidebar:

Automatically creates a table

Table name = file name

Instantly queryable via natural language

🔐 Security

Only SELECT queries allowed

Blocks:

DELETE

DROP

UPDATE

INSERT

ALTER

TRUNCATE

Automatic LIMIT injection (default: 100 rows)

SQL syntax repair layer

🧠 AI Prompt Rules

The model is instructed to:

Use only existing tables

Output only valid SQLite SQL

Never modify data

No explanations

🛠 Tech Stack
Layer	Tech
AI -->	Ollama + LLaMA 3
Backend -->	FastAPI
Database -->	SQLite
Frontend -->	Streamlit
Charts -->	Matplotlib
Data -->	Pandas
