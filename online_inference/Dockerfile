FROM python:3.9-slim

COPY . .

# setup package
RUN pip install --upgrade pip
RUN pip install -e .

CMD ["uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000"]