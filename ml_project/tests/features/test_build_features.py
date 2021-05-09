from heart_disease_source_code.features.build_features import *
import pytest


def test_can_check_raw_data(train_data_sample):
    assert set(train_data_sample.columns) == {
        'age','ca','chol','cp','exang','fbs','oldpeak',
        'restecg','sex','slope','target','thal','thalach','trestbps'
    }
    check_raw_data(train_data_sample)


def test_raise_bad_columns(train_data_sample):
    train_data_broken = train_data_sample.rename(columns={'age': 'birthdate'})
    with pytest.raises(Exception) as e_info:
        check_raw_data(train_data_broken)

    train_data_broken = train_data_sample.drop(columns={'target'})
    with pytest.raises(Exception) as e_info:
        check_raw_data(train_data_broken)


def test_can_rename_columns(train_data_sample):
    rename_columns(train_data_sample)


def test_can_make_human_readable_categories(train_data_sample):
    train_data_sample = rename_columns(train_data_sample)
    make_human_readable_categories(train_data_sample)


def test_can_process_categorical_features(train_data_sample):
    train_data_sample = rename_columns(train_data_sample)
    train_data_sample = make_human_readable_categories(train_data_sample)

    process_categorical_features(train_data_sample)


def test_can_preprocess_raw_data(train_data_sample):
    transformer = PreprocessRawData()
    train_data_transformed = transformer.fit_transform(train_data_sample)
    expected_columns_cnt = 30
    assert expected_columns_cnt == train_data_transformed.shape[1]

    expected_columns = ['age', 'resting_blood_pressure', 'cholesterol',
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

    assert set(expected_columns) == set(train_data_transformed.columns)





