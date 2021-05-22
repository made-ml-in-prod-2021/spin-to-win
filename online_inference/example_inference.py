import pandas as pd
import json
import requests
import logging

logger = logging.getLogger(__name__)

DATA_PATH = "data/raw/example_for_online_inference.csv"


def main():
    data = pd.read_csv(DATA_PATH).to_dict(orient="records")

    for row in data:
        response = requests.post(
            "http://0.0.0.0:8000/predict",
            json.dumps(row)
        )
        logger.info(response)
        logger.info(response.text)


if __name__ == "__main__":
    main()