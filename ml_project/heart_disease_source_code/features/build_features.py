import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import TransformerMixin


class PreprocessRawData(TransformerMixin):

    def __init__(self):
        pass

    def fit(self, df):
        return self

    def transform(self, df):
        df = check_raw_data(df)
        df = rename_columns(df)
        df = make_human_readable_categories(df)
        df = process_categorical_features(df)

        # One Hot Encoding
        df = pd.get_dummies(df, drop_first=False)

        return df


def check_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Кидаем ошибку, если в Raw Data неожиданные колонки """

    expected_cols = [
        'age','ca','chol','cp','exang','fbs','oldpeak',
        'restecg','sex','slope','target','thal','thalach','trestbps'
    ]
    expected_cols = sorted(set(expected_cols))
    input_cols = sorted(set(df.columns))

    assert expected_cols == input_cols, (
        f'input columns dont match expected: \n input: {input_cols} \n expected: {expected_cols}'
    )

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        'age': 'age', 
        'sex': 'sex', 
        'cp': 'chest_pain_type', 
        'trestbps': 'resting_blood_pressure', 
        'chol': 'cholesterol', 
        'fbs': 'fasting_blood_sugar', 
        'restecg': 'rest_ecg', 
        'thalach': 'max_heart_rate_achieved', 
        'exang': 'exercise_induced_angina', 
        'oldpeak': 'st_depression', 
        'slope': 'st_slope', 
        'ca': 'num_major_vessels', 
        'thal': 'thalassemia', 
        'target': 'target', 
    })
    return df


def make_human_readable_categories(df: pd.DataFrame) -> pd.DataFrame:

    df['sex'][df['sex'] == 0] = 'female'
    df['sex'][df['sex'] == 1] = 'male'

    df['chest_pain_type'][df['chest_pain_type'] == 0] = 'no'
    df['chest_pain_type'][df['chest_pain_type'] == 1] = 'typical_angina'
    df['chest_pain_type'][df['chest_pain_type'] == 2] = 'atypical_angina'
    df['chest_pain_type'][df['chest_pain_type'] == 3] = 'non_anginal_pain'
    df['chest_pain_type'][df['chest_pain_type'] == 4] = 'asymptomatic'

    df['fasting_blood_sugar'][df['fasting_blood_sugar'] == 0] = 'low'
    df['fasting_blood_sugar'][df['fasting_blood_sugar'] == 1] = 'high'

    df['rest_ecg'][df['rest_ecg'] == 0] = 'normal'
    df['rest_ecg'][df['rest_ecg'] == 1] = 'wave_abnormality'
    df['rest_ecg'][df['rest_ecg'] == 2] = 'hypertrophy'

    df['exercise_induced_angina'][df['exercise_induced_angina'] == 0] = 'no'
    df['exercise_induced_angina'][df['exercise_induced_angina'] == 1] = 'yes'

    df['st_slope'][df['st_slope'] == 0] = 'no'
    df['st_slope'][df['st_slope'] == 1] = 'upsloping'
    df['st_slope'][df['st_slope'] == 2] = 'flat'
    df['st_slope'][df['st_slope'] == 3] = 'downsloping'

    df['thalassemia'][df['thalassemia'] == 0] = 'no'
    df['thalassemia'][df['thalassemia'] == 1] = 'normal'
    df['thalassemia'][df['thalassemia'] == 2] = 'fixed_defect'
    df['thalassemia'][df['thalassemia'] == 3] = 'reversable_defect'

    return df

def process_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """ Заполнить пропуски и задать категории

    Небольшой дисклеймер: Когда категорий мало, я предпочитаю явно 
    выписать все трансформации, чем юзать трансформеры. 

    В данной конкретной задаче с помощью ручной обработки я увидел
    , что есть пустые категории:
    - st_slope_downsloping
    - chest_pain_type_asymptomatic

    В будущем, если датасет увеличится и пустые категории заполнятся, 
    такой ручной пайплайн не сломается, в отличие от автоматических трансформеров 
    из склерна

    """

    df['sex'] = df['sex'].fillna('other').astype(
        CategoricalDtype(['female', 'male', 'other'])
    )
    df['chest_pain_type'] = df['chest_pain_type'].fillna('no').astype(
        CategoricalDtype(['atypical_angina', 'no', 'non_anginal_pain', 'typical_angina', 'asymptomatic'])
    )
    df['fasting_blood_sugar'] = df['fasting_blood_sugar'].fillna('low').astype(
        CategoricalDtype(['high', 'low'])
    )
    df['rest_ecg'] = df['rest_ecg'].fillna('normal').astype(
        CategoricalDtype(['hypertrophy', 'normal', 'wave_abnormality'])
    )
    df['exercise_induced_angina'] = df['exercise_induced_angina'].fillna('no').astype(
        CategoricalDtype(['no', 'yes'])
    )
    df['st_slope'] = df['st_slope'].fillna('no').astype(
        CategoricalDtype(['flat', 'no', 'upsloping', 'downsloping'])
    )
    df['thalassemia'] = df['thalassemia'].fillna('no').astype(
        CategoricalDtype(['fixed_defect', 'no', 'normal', 'reversable_defect'])
    )
    return df




