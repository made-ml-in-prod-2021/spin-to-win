import os
import pandas as pd
import numpy as np
import pytest
from typing import List
from faker import Faker

fake = Faker('en_US')
Faker.seed(4321)


@pytest.fixture()
def expected_columns():
    expected_columns = [
       'age', 'resting_blood_pressure', 'cholesterol',
       'max_heart_rate_achieved', 'st_depression', 'num_major_vessels',
       'target', 'sex_female', 'sex_male', 'sex_other',
       'chest_pain_type_atypical_angina', 'chest_pain_type_no',
       'chest_pain_type_non_anginal_pain', 'chest_pain_type_typical_angina',
       'chest_pain_type_asymptomatic', 'fasting_blood_sugar_high',
       'fasting_blood_sugar_low', 'rest_ecg_hypertrophy', 'rest_ecg_normal',
       'rest_ecg_wave_abnormality', 'exercise_induced_angina_no',
       'exercise_induced_angina_yes', 'st_slope_flat', 'st_slope_no',
       'st_slope_upsloping', 'st_slope_downsloping',
       'thalassemia_fixed_defect', 'thalassemia_no', 'thalassemia_normal',
       'thalassemia_reversable_defect'
    ]
    return expected_columns


@pytest.fixture()
def dataset_path():
    curdir = os.path.dirname(__file__)
    return os.path.join(curdir, "train_data_sample.csv")


@pytest.fixture()
def train_data_sample(dataset_path):
    df = pd.read_csv(dataset_path)
    return df


@pytest.fixture()
def fake_data():
    sample_size = 500
    np.random.seed(10)
    df = pd.DataFrame({
        'fake_name': [fake.name() for _ in range(sample_size)],
        'fake_location': [fake.address() for _ in range(sample_size)],
        'fake_birthdate': [fake.date() for _ in range(sample_size)],
        'age': np.random.randint(0, 100, size=sample_size),
        'cp': np.random.randint(4, size=sample_size),
        'sex': np.random.randint(2, size=sample_size),
        'trestbps': np.random.randint(94, 200, size=sample_size),
        'chol': np.random.randint(126, 564, size=sample_size),
        'fbs': np.random.randint(2, size=sample_size),
        'restecg': np.random.randint(2, size=sample_size),
        'thalach': np.random.randint(71, 202, size=sample_size),
        'exang': np.random.randint(2, size=sample_size),
        'oldpeak': [fake.pyfloat(min_value=0, max_value=7) for _ in range(sample_size)],
        'slope': np.random.randint(3, size=sample_size),
        'ca': np.random.randint(5, size=sample_size),
        'thal': np.random.randint(4, size=sample_size),
        'target': np.random.randint(2, size=sample_size),
    })
    return df

