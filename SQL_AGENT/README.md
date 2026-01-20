# NLP → SQL (FastAPI + Streamlit)

## Structure

backend/   - FastAPI API server
frontend/  - Streamlit UI
requirements.txt

## Run Backend

cd backend
uvicorn main:app --reload

## Run Frontend

cd frontend
streamlit run app.py

## Run Tests

```bash
cd backend
pytest
```
