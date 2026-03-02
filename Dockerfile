FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
 