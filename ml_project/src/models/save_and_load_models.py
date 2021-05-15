import pandas as pd
import pickle
import logging
import os

logger = logging.getLogger(__name__)

def serialize_model(model_path, model, transformer, selected_features):
    os.makedirs(model_path, exist_ok=True)

    logger.info("save classifier")
    clf_path = os.path.join(model_path, 'clf.pkl')
    with open(clf_path, "wb") as f:
        pickle.dump(model, f)

    logger.info("save transformer")
    transformer_path = os.path.join(model_path, 'transformer.pkl')
    with open(transformer_path, "wb") as f:
        pickle.dump(transformer, f)

    logger.info("save selected_features")
    feats_path = os.path.join(model_path, 'train_features.txt')
    pd.DataFrame(columns=selected_features).to_csv(feats_path, index=False)


def load_model(model_path):
    logger.info("load classifier")
    clf_path = os.path.join(model_path, 'clf.pkl')
    with open(clf_path, "rb") as f:
        model = pickle.load(f)
    
    logger.info("load transformer")
    transformer_path = os.path.join(model_path, 'transformer.pkl')
    with open(transformer_path, "rb") as f:
        transformer = pickle.load(f)

    logger.info("load selected_features")
    feats_path = os.path.join(model_path, 'train_features.txt')
    selected_features = pd.read_csv(feats_path).columns.tolist()

    return model, transformer, selected_features

