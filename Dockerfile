FROM python:3.11-alpine
WORKDIR /app
RUN: python -m pip install -r requirements.txt
COPY requirements.txt .
COPY . .
EXPOSE 8000
CMD ["python","main.py"]
