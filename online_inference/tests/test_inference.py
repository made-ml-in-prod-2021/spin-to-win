import pytest
from fastapi.testclient import TestClient
import pandas as pd

from app import app

DATA_PATH = "data/raw/example_for_online_inference.csv"


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def example_data():
    return pd.read_csv(DATA_PATH).to_dict(orient="records")


@pytest.fixture
def example_row(example_data):
    return example_data[5]


def test_startup(client):
    resp = client.get("/healthcheck")
    assert 200 == resp.status_code


def test_root(client):
    resp = client.get("/")
    assert 200 == resp.status_code


def test_normal_data_return_200_status(example_row, client):
    resp = client.post("/predict", json=example_row)
    assert 200 == resp.status_code


def test_data_validation_return_400_status_if_bad_range(example_row, client):
    example_row['age'] = 234
    resp = client.post("/predict", json=example_row)
    assert 400 == resp.status_code


def test_data_validation_return_400_status_if_not_binary(example_row, client):
    example_row['sex'] = 2
    resp = client.post("/predict", json=example_row)
    assert 400 == resp.status_code


def test_data_validation_return_400_status_if_bad_category(example_row, client):
    example_row['slope'] = 9
    resp = client.post("/predict", json=example_row)
    assert 400 == resp.status_code


def test_normal_data_return_200_multiple_rows(example_data, client):
    for row in example_data:
        resp = client.post("/predict", json=row)
        assert 200 == resp.status_code




