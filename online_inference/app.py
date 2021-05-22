import sys
import os
import uuid
import logging
import uvicorn
import pandas as pd
from fastapi import FastAPI

from src.models.save_and_load_models import load_model
from src.entities.data_validation import HeartDiseaseResponse, HeartDiseaseRequest
from src.setup_logger import setup_logger

logger = setup_logger(__name__) # logging.getLogger(__name__)

app = FastAPI()

classifier, transformer, train_features = None, None, None


@app.on_event("startup")
def load_model_startup():
    """ Load baseline model """
    global classifier, transformer, train_features

    model_path = os.getenv("PATH_TO_MODEL") or './models/baseline_model_v1'
    try:
        classifier, transformer, train_features = load_model(model_path)
    except FileNotFoundError as e:
        classifier, transformer, train_features = None, None, None
        logger.error(e)
        raise RuntimeError(e)


@app.get("/healthcheck")
def healthcheck() -> bool:
    return not (classifier is None)


@app.get("/")
async def root():
    """ root-page """
    return {"Hello": "world"}


@app.api_route("/predict", response_model=HeartDiseaseResponse, methods=["POST"])
def predict(data: HeartDiseaseRequest) -> HeartDiseaseResponse:

    if not healthcheck():
        raise HTTPException(status_code=500, detail="healthcheck: False")

    sample_uuid = data.uuid if 'uuid' in data else uuid.uuid4()
    df = pd.DataFrame.from_dict([data.dict()])
    data_processed = transformer.transform(df)
    proba = classifier.predict_proba(data_processed[train_features])[:, 1]

    return HeartDiseaseResponse(uuid=sample_uuid, proba=proba) 


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=os.getenv("PORT", 8001))



