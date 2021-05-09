import os
import pandas as pd
import pytest
from typing import List


@pytest.fixture()
def dataset_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "train_data_sample.csv")


@pytest.fixture()
def train_data_sample(dataset_path):
    df = pd.read_csv(dataset_path)
    return df


