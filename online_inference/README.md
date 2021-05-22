hw # 2 online inference 

Основные архитектурные решения:
 - FastAPI - потому что автоматом генерируются нереально крутые доки! 
 - валидация входных данных на Pydantic (см. src.entities.data_validation.py)
 - кастомный трансформер, который дружит с pickle. Для этого скопировал папку src из первого дз (pickle не может загрузить объект, если код для его создания лежит в другом проекте)
 - докер весит всего 227 МБ. Для этого использовал python:3.9-slim и радикально сократил число слоев и библиотек
 - образ лежит в docker hub (docker push spintowin/heart-dis:v1)


docker 
```
docker build -t spintowin/heart-dis:v1 .
docker run -p 8000:8000 spintowin/heart-dis:v1
# then go to http://localhost:8000 or use this .py script:
python example_requests.py
```

local run (http://localhost:8000/)
```
python -m venv .venv
source .venv/bin/activate
pip install -e  .
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API documentation:
```
http://localhost:8000/docs
```

Тесты
```pytest -v```




Самооценка: 22 балла

1. ✅ ветку назовите homework2, положите код в папку online_inference
2. ✅ Оберните inference вашей модели в rest сервис, должен быть endpoint /predict (3 балла)
3. ✅ Напишите тест для /predict (3 балла) 
4. ✅ Напишите скрипт, который будет делать запросы к вашему сервису -- 2 балла
5. ✅ Сделайте валидацию входных данных  -- 3 доп балла
6. ✅ Напишите dockerfile, соберите на его основе образ и запустите локально контейнер (docker build, docker run), внутри контейнера должен запускать сервис, написанный в предущем пункте, закоммитьте его, напишите в readme корректную команду сборки (4 балл)
7. ✅ Оптимизируйте размер docker image (3 доп балла) 
8. ✅ опубликуйте образ в [https://hub.docker.com/](https://hub.docker.com/), используя docker push (2 балла)
9. ✅ напишите в readme корректные команды docker pull/run, которые должны привести к тому, что локально поднимется на inference ваша модель (1 балл)
10. ✅ проведите самооценку -- 1 доп балл
11. ✅ создайте пулл-реквест и поставьте label -- hw2



