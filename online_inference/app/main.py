import os
import pandas as pd
from fastapi import FastAPI
import logging

from app.utils.save_and_load_models import load_model

BASELINE_MODEL = './models/baseline_model_v1'

logger = logging.getLogger(__name__)

transformer = None
classifier = None
train_features = None

app = FastAPI()


@app.on_event("startup")
def load_model_startup():
    """ Load baseline model """
    global transformer
    global classifier
    global train_features

    try:
        transformer, classifier, train_features = load_model(BASELINE_MODEL)
    except FileNotFoundError as e:
        logger.error(e)
        transformer, classifier, train_features = None, None, None
        return


@app.get("/")
async def root():
    """ root-page """
    return {"Hello": "World"}














