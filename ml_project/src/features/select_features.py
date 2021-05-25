import numpy as np
import pandas as pd

def select_features(df, strategy='default'):

    if strategy == 'default':
        empty_features = ['st_slope_downsloping', 'chest_pain_type_asymptomatic', 'sex_other']
        drops = ['target']
        selected_features = [
            i for i in df.columns if i not in empty_features and i not in drops
        ]
        return selected_features
    else:
        raise NotImplementedError(
            'Custom feature selection strategies is not available in this version'
        )
