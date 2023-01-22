FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./config ./config
COPY ./src ./src
COPY .env .
COPY main.py .

CMD ["python", "main.py"]