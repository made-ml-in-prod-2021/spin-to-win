import os 
import sys
import click
import hydra
from omegaconf import OmegaConf
import pandas as pd
import pickle
import logging

from heart_disease_source_code.data import read_data, split_train_val_data
from heart_disease_source_code.features.build_features import PreprocessRawData

import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

logger = logging.getLogger(__name__)


def train_pipeline(training_params):

    # 1. read data
    logger.info(f"start train pipeline with params {training_params}")
    data = read_data(training_params.input_data_path)
    logger.info(f"data.shape is {data.shape}")

    # 2. split strategy
    X_train, X_val = split_train_val_data(
        data, training_params.splitting_strategy, training_params.splitting_params
    )
    logger.info(f"X_train.shape is {X_train.shape} X_val.shape is {X_val.shape}")

    # 3. preprocess data
    logger.info("preprocess data...")
    transformer = PreprocessRawData()
    X_train = transformer.fit_transform(X_train)
    X_val = transformer.transform(X_val)

    if training_params.model.train_params.train_features == 'default':
        empty_features = {'st_slope_downsloping', 'chest_pain_type_asymptomatic', 'sex_other'}
        train_features = [i for i in X_train.columns if i not in empty_features and i != 'target']
    else:
        train_features = training_params.model.train_params.train_features
        assert isinstance(train_features, list)

    # 4. train 
    if training_params.model.name == "rf":
        model = RandomForestClassifier(**training_params.model.train_params.model_params)
    elif training_params.model.name == "lr":
        model = LogisticRegression(**training_params.model.train_params.model_params)
    else:
        raise NotImplementedError()

    logger.info("fit model...")
    model.fit(X_train[train_features], X_train['target'])

    # 5. save model 
    if training_params.serialize_model == True:
        with open(training_params.output_model_path, "wb") as f:
            pickle.dump(model, f)

    # 4. validate
    if len(X_val) == 0:
        val_preds = None
    else:
        val_preds = model.predict_proba(X_val[train_features])[:, 1]

    train_preds = model.predict_proba(X_train[train_features])[:, 1]
    train_score = roc_auc_score(X_train['target'], train_preds)
    val_score = roc_auc_score(X_val['target'], val_preds) if val_preds \
                is not None else np.NaN
    logger.info(f'ROC AUC train: {train_score:.5f} val: {val_score:.5f}')

    return model, transformer, train_features


def predict_new_data(
    predict_raw_data_path, predict_out_data_path, 
    model, transformer, train_features
    ):
    X_test = read_data(predict_raw_data_path)
    X_test = transformer.transform(X_test)
    
    test_preds = model.predict_proba(X_test[train_features])[:, 1]
    test_preds_df = pd.DataFrame(data=test_preds, columns=['preds'])
    test_preds_df.to_csv(predict_out_data_path, index=False)


@hydra.main(config_path='../config', config_name='train_config')
def main(cfg):

    cfg.input_data_path = hydra.utils.to_absolute_path(cfg.input_data_path)
    cfg.output_model_path = hydra.utils.to_absolute_path(cfg.output_model_path)
    cfg.predict_raw_data_path = hydra.utils.to_absolute_path(cfg.predict_raw_data_path)
    cfg.predict_out_data_path = hydra.utils.to_absolute_path(cfg.predict_out_data_path)

    logger.info(OmegaConf.to_yaml(cfg))

    model, transformer, train_features = train_pipeline(cfg)
    
    if cfg.predict_raw_data_path is not None:
        result = predict_new_data(
            cfg.predict_raw_data_path, cfg.predict_out_data_path, 
            model, transformer, train_features
        )


if __name__ == "__main__":
    main()











