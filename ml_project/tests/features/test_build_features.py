from src.features.build_features import *
import pytest


def test_can_check_raw_data(train_data_sample):
    assert set(train_data_sample.columns) == {
        'age','ca','chol','cp','exang','fbs','oldpeak',
        'restecg','sex','slope','target','thal','thalach','trestbps'
    }
    PreprocessRawData.check_raw_data(train_data_sample)

    train_data_sample['new_feature_that_should_not_raise'] = 123
    PreprocessRawData.check_raw_data(train_data_sample)


def test_raise_if_bad_columns(train_data_sample):
    train_data_broken = train_data_sample.rename(columns={'age': 'birthdate'})
    with pytest.raises(Exception) as e_info:
        PreprocessRawData.check_raw_data(train_data_broken)

    train_data_broken = train_data_sample.drop(columns={'target'})
    with pytest.raises(Exception) as e_info:
        PreprocessRawData.check_raw_data(train_data_broken)


def test_can_select_usefull_columns(train_data_sample):
    PreprocessRawData.select_needed_columns(train_data_sample)

def test_can_rename_columns(train_data_sample):
    preprocessed = PreprocessRawData.select_needed_columns(train_data_sample)
    PreprocessRawData.rename_columns(preprocessed)


def test_can_make_human_readable_categories(train_data_sample):
    preprocessed = PreprocessRawData.select_needed_columns(train_data_sample)
    preprocessed = PreprocessRawData.rename_columns(preprocessed)
    PreprocessRawData.make_human_readable_categories(preprocessed)


def test_can_process_categorical_features(train_data_sample):
    preprocessed = PreprocessRawData.select_needed_columns(train_data_sample)
    preprocessed = PreprocessRawData.rename_columns(preprocessed)
    preprocessed = PreprocessRawData.make_human_readable_categories(preprocessed)
    PreprocessRawData.process_categorical_features(preprocessed)


def test_can_preprocess_raw_data(train_data_sample, expected_columns):
    transformer = PreprocessRawData()
    train_data_transformed = transformer.fit_transform(train_data_sample)
    assert set(expected_columns) == set(train_data_transformed.columns)


def test_can_preprocess_fake_data(fake_data, expected_columns):
    transformer = PreprocessRawData()
    train_data_transformed = transformer.fit_transform(fake_data)
    assert all([i in train_data_transformed.columns for i in expected_columns])



