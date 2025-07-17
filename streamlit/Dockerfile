FROM python:3.11-slim

WORKDIR /app

COPY ./streamlit .

COPY ./core ./core

COPY ./models ./models

RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
