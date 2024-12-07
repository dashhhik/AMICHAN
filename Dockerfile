FROM node:20-alpine AS frontend-build

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt version.py ./

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install uvicorn


ENV PYTHONPATH "${PYTHONPATH}:/amichan"

COPY . ./

EXPOSE 8000