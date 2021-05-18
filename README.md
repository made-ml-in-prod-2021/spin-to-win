# spin-to-win
telegram: spin_to_win

Установка:
```
python -m venv .venv
source .venv/bin/activate
pip install -e  .
```

Обучение (на дефолтном конфиге):
```
python heart_disease_source_code/train.py
```

Дефолтный конфиг (Hydra):
```
ml_example/config/train_config.yaml
```

Изменение параметпров обучение in place:
```
python src/train.py model=logreg
python src/train.py model=forest model.train_params.model_params.n_estimators=400
```

Предикт (без пере-обучения модели):
```
python src/train.py \
  fit_model=False \
  serialize_model=False \
  predict_raw_data_path='data/raw/example_for_predict.csv' \
  predict_out_data_path='data/output/example_predicts.csv'
```

Тесты
```
python -m pytest -v
```

Самооценка:
Я сделал все пункты кроме 7 и 12 из чеклиста https://data.mail.ru/blog/topic/view/18519/
Соответственно вернхяя оценка 30 баллов, без учета штрафов за косяки, замечения, ошибки ну и так далее - это отдаю на суд ревьюера

Основные архитектурные решения:
- сохранение модели, трансформатора и списка отобранных фич - все в отдельную папку. Например, models/baseline_model_v1/. Соответственно новая модель = новая папка, нельзя заливать несколько моделей в одну папку!
- конфигурирование через Hydra 

P.S. добавил коммит "hw#1 bugfix 5"
- исправил bug из-за которого неправильно настроенный gitignore не заливал часть папок в гит - в том числе папку с ноутбуком.
- переписал сохранение модели
