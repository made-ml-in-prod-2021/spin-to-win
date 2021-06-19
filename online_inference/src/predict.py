import os  
import hydra
from omegaconf import OmegaConf
import pandas as pd
pd.options.mode.chained_assignment = None
import logging

from src.data import read_data
from src.models.save_and_load_models import load_model

logger = logging.getLogger(__name__)


def predict_pipeline(cfg):
    assert os.path.exists(cfg.model_path)

    logger.info("loading model for predict...")
    model, transformer, selected_features = load_model(cfg.model_path)

    X_test = read_data(cfg.predict_raw_data_path)
    X_test = transformer.transform(X_test)
    
    logger.info("predict probabilities")
    test_preds = model.predict_proba(X_test[selected_features])[:, 1]
    test_preds_df = pd.DataFrame(data=test_preds, columns=['preds'])

    logger.info(f"save predicts to {cfg.predict_out_data_path}")
    test_preds_df.to_csv(cfg.predict_out_data_path, index=False)


@hydra.main(config_path='../config', config_name='test_config')
def main(cfg):

    # hydra doesn't work with relative paths
    cfg.model_path = hydra.utils.to_absolute_path(cfg.model_path)
    cfg.predict_raw_data_path = hydra.utils.to_absolute_path(cfg.predict_raw_data_path)
    cfg.predict_out_data_path = hydra.utils.to_absolute_path(cfg.predict_out_data_path)
    
    predict_pipeline(cfg)


if __name__ == "__main__":
    main()











