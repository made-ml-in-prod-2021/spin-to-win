online inference:

docker 
```
docker build -t heart-dis:v1 .
docker run -p 8000:8000 heart-dis .
# then go to http://localhost:8000 or use this .py script:
python example_requests.py
```

local run (http://localhost:8000/)
```
python -m venv .venv
source .venv/bin/activate
pip install -e  .
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```


