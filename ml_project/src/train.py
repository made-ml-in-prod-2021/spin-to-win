import os 
import sys
import click
import hydra
from omegaconf import OmegaConf
import pandas as pd
import pickle
import logging
from pprint import pprint

from src.data import read_data, split_train_val_data
from src.features.build_features import PreprocessRawData
from src.features.select_features import select_features
from src.models.save_and_load_models import serialize_model, load_model

import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

logger = logging.getLogger(__name__)

def train_pipeline(cfg):

    # 1. read data
    logger.info(f"start train pipeline with config: \n\n{OmegaConf.to_yaml(cfg)} \n")

    data = read_data(cfg.input_data_path)
    logger.info(f"data.shape is {data.shape}")

    # 2. split strategy
    X_train, X_val = split_train_val_data(
        data, cfg.splitting_strategy, cfg.splitting_params
    )
    logger.info(f"X_train.shape is {X_train.shape} X_val.shape is {X_val.shape}")

    # 3. preprocess data
    logger.info("preprocess data...")
    transformer = PreprocessRawData()
    X_train = transformer.fit_transform(X_train)
    X_val = transformer.transform(X_val)

    selected_features = select_features(X_train, strategy='default')

    # 4. train 
    if cfg.model.name == "rf":
        model = RandomForestClassifier(**cfg.model.train_params.model_params)
    elif cfg.model.name == "lr":
        model = LogisticRegression(**cfg.model.train_params.model_params)
    else:
        raise NotImplementedError()

    if cfg.fit_model:
        logger.info("fit model")
        model.fit(X_train[selected_features], X_train['target'])

    # 5. save model 
    if cfg.fit_model == False and cfg.serialize_model == True:
        assert 1 == 0, ('you`re trying to save model without fit() it!')

    if cfg.serialize_model:
        serialize_model(cfg.model_path, model, transformer, selected_features)

    # 4. validate
    logger.info("load model for validation")
    model, transformer, selected_features = load_model(cfg.model_path)

    train_preds = model.predict_proba(X_train[selected_features])[:, 1]
    train_score = roc_auc_score(X_train['target'], train_preds)

    if len(X_val) == 0:
        val_preds = None
        val_score = np.NaN
    else:
        val_preds = model.predict_proba(X_val[selected_features])[:, 1]
        val_score = roc_auc_score(X_val['target'], val_preds)

    logger.info(f'ROC AUC train: {train_score:.5f} val: {val_score:.5f}')

    return transformer, selected_features


def predict_new_data(
    predict_raw_data_path, model_path, predict_out_data_path, 
    transformer, selected_features
    ):
    assert os.path.exists(model_path)

    logger.info("load model for predict")
    model, transformer, selected_features = load_model(model_path)

    X_test = read_data(predict_raw_data_path)
    X_test = transformer.transform(X_test)
    
    logger.info("predict probabilities")
    test_preds = model.predict_proba(X_test[selected_features])[:, 1]
    test_preds_df = pd.DataFrame(data=test_preds, columns=['preds'])
    logger.info("save predicts to csv")
    test_preds_df.to_csv(predict_out_data_path, index=False)


@hydra.main(config_path='../config', config_name='train_config')
def main(cfg):

    # hydra doesn't work with relative paths
    cfg.input_data_path = hydra.utils.to_absolute_path(cfg.input_data_path)
    cfg.model_path = hydra.utils.to_absolute_path(cfg.model_path)
    cfg.predict_raw_data_path = hydra.utils.to_absolute_path(cfg.predict_raw_data_path)
    cfg.predict_out_data_path = hydra.utils.to_absolute_path(cfg.predict_out_data_path)

    transformer, selected_features = train_pipeline(cfg)
    
    if cfg.predict_raw_data_path is not None:
        predict_new_data(
            cfg.predict_raw_data_path, cfg.model_path, cfg.predict_out_data_path, 
            transformer, selected_features
        )


if __name__ == "__main__":
    main()











