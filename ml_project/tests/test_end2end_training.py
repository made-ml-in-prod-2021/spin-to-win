import os
import yaml
from argparse import Namespace
import logging
from omegaconf import OmegaConf
import warnings
warnings.filterwarnings("ignore")

from src.train import train_pipeline
from src.predict import predict_pipeline


def test_train_e2e(tmpdir, dataset_path, caplog):
    caplog.set_level(logging.INFO)

    params = {
        'fit_model': True, 
        'input_data_path': 'data/raw/heart.csv', 
        'serialize_model': True, 
        'model_path': 'models/baseline_model_v1/', 
        'splitting_strategy': 'holdout', 
        'splitting_params': {
            'val_size': 0.1, 
            'random_state': 3
        }, 
        'predict_raw_data_path': 'data/raw/example_for_predict.csv', 
        'predict_out_data_path': 'data/output/example_predicts.csv', 
        'model': {
            'name': 'rf', 
            'train_params': {
                'selected_features': 'default', 
                'model_params': {
                    'n_estimators': 120, 
                    'random_state': 10, 
                    'max_depth': None
                }
            }
        }
    }
    cfg = yaml.dump(params)
    cfg = OmegaConf.create(cfg)

    train_pipeline(cfg)
    
    log1 = "start train pipeline"
    log2 = "preprocess data"
    log3 = "fit model"
    log4 = "ROC AUC train"
    assert 1 == sum([1 for i in caplog.records if log1 in i.message])
    assert 1 == sum([1 for i in caplog.records if log2 in i.message])
    assert 1 == sum([1 for i in caplog.records if log3 in i.message])
    assert 1 == sum([1 for i in caplog.records if log4 in i.message])

def test_predict_e2e(tmpdir, dataset_path, caplog):
    caplog.set_level(logging.INFO)

    params = {
        'model_path': 'models/baseline_model_v1/', 
        'predict_raw_data_path': 'data/raw/example_for_predict.csv', 
        'predict_out_data_path': 'data/output/example_predicts.csv', 
    }
    cfg = yaml.dump(params)
    cfg = OmegaConf.create(cfg)

    predict_pipeline(cfg)
    
    # log1 = "start train pipeline"
    # log2 = "preprocess data"
    # log3 = "fit model"
    # log4 = "ROC AUC train"
    # assert 1 == sum([1 for i in caplog.records if log1 in i.message])
    # assert 1 == sum([1 for i in caplog.records if log2 in i.message])
    # assert 1 == sum([1 for i in caplog.records if log3 in i.message])
    # assert 1 == sum([1 for i in caplog.records if log4 in i.message])

