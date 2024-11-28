FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt version.py ./

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install uvicorn


ENV PYTHONPATH "${PYTHONPATH}:/amichan"

COPY . ./

EXPOSE 8000
