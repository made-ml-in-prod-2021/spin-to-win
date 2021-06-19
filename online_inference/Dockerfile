FROM python:3.9-slim

COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

WORKDIR .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
