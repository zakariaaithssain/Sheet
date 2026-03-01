FROM python:3.13-slim

WORKDIR /app

#c compiler might be needed for some packages
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
 