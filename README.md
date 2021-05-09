# spin-to-win
telegram: spin_to_win

Установка:
python -m venv .venv
source .venv/bin/activate
pip install -e  .

Обучение:
python heart_disease_source_code/train.py
python heart_disease_source_code/train.py model=logreg
python heart_disease_source_code/train.py model=forest 
python heart_disease_source_code/train.py model=forest model.train_params.model_params.n_estimators=4

Дефолтный конфиг:
ml_example/config/train_config.yaml

Предикт (без обучения):
python heart_disease_source_code/train.py \
  fit_model=False \
  serialize_model=False \
  predict_raw_data_path='data/raw/example_for_predict.csv' \
  predict_out_data_path='data/output/example_predicts.csv'

Тесты
python -m pytest -v
