FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
