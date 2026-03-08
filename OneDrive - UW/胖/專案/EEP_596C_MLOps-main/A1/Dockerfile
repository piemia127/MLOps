FROM python:3.10-slim

WORKDIR /app

COPY ./app ./app
COPY requirements.txt .
COPY model.pkl .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
