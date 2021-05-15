# -*- coding: utf-8 -*-
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def read_data(path):
    data = pd.read_csv(path)
    return data


def split_train_val_data(data, strategy, params):

    if strategy == 'holdout' :
        train_data, val_data = train_test_split(
            data, test_size=params.val_size, random_state=params.random_state
        )
    elif strategy is None:
        train_data = data
        val_data = pd.DataFrame(columns=data.columns) # empty df
    else:
        NotImplementedError()

    return train_data, val_data








