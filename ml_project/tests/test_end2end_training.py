import os
import yaml
from argparse import Namespace
import logging
from omegaconf import OmegaConf
import warnings
warnings.filterwarnings("ignore")

from src.train import train_pipeline, predict_new_data


def test_train_e2e(tmpdir, dataset_path, caplog):
    caplog.set_level(logging.INFO)

    expected_output_model_path = tmpdir.join("model.pkl")
    expected_metric_path = tmpdir.join("metrics.json")
    
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

    transformer, selected_features = train_pipeline(cfg)
    
    if cfg.predict_raw_data_path is not None:
        predict_new_data(
            cfg.predict_raw_data_path, cfg.model_path, cfg.predict_out_data_path, 
            transformer, selected_features
        )
    
    log1 = "start train pipeline"
    log2 = "preprocess data"
    log3 = "fit model"
    log4 = "ROC AUC train"
    assert 1 == sum([1 for i in caplog.records if log1 in i.message])
    assert 1 == sum([1 for i in caplog.records if log2 in i.message])
    assert 1 == sum([1 for i in caplog.records if log3 in i.message])
    assert 1 == sum([1 for i in caplog.records if log4 in i.message])

