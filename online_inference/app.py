import sys
import os
import pandas as pd
from fastapi import FastAPI
import logging

from src.models.save_and_load_models import load_model

logger = logging.getLogger(__name__)

app = FastAPI()

transformer, classifier, train_features = None, None, None

@app.on_event("startup")
def load_model_startup():
    """ Load baseline model """
    global transformer, classifier, train_features

    model_path = os.getenv("PATH_TO_MODEL") or './models/baseline_model_v1'
    try:
        transformer, classifier, train_features = load_model(model_path)
    except FileNotFoundError as e:
        logger.error(e)
        transformer, classifier, train_features = None, None, None
        raise RuntimeError(e)


@app.get("/healthcheck")
def healthcheck() -> bool:
    return not (classifier is None)


@app.get("/")
async def root():
    """ root-page """
    return {"Hello": "world"}





