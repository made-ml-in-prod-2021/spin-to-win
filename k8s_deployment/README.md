## 1
Разверните kubernetes

```$ gcloud container clusters get-credentials cluster-2 --zone us-central1-c --project vaulted-cogency-317309```


```$ kubectl cluster-info```

```
Kubernetes master is running at https://35.184.174.105
GLBCDefaultBackend is running at https://35.184.174.105/api/v1/namespaces/kube-system/services/default-http-backend:http/proxy
KubeDNS is running at https://35.184.174.105/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://35.184.174.105/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## 2 
Напишите простой pod manifests для вашего приложения, назовите его online-inference-pod.yaml

Задеплойте приложение в кластер (kubectl apply -f online-inference-pod.yaml), убедитесь, что все поднялось (kubectl get pods)

```$ kubectl apply -f ./k8s_deployment/online-inference-pod.yaml```

```$ kubectl get pods```
```
NAME               READY   STATUS    RESTARTS   AGE
online-inference   1/1     Running   0          34m
```

Приложите скриншот, где видно, что все поднялось

[url=https://radikal.ru/big/26w4fb6hm2ct1][img]https://c.radikal.ru/c22/2106/24/85992c6f92d4t.jpg[/img][/url]


## 2a 
Пропишите requests/limits и напишите зачем это нужно в описание PR

закоммитьте файл online-inference-pod-resources.yaml

requests отвечает за гарантированные ресурсы, которые будут доступны внутри контейнера. 

limits отвечает за предельные значения ресурсов, которые может потребовать контейнер. 

Если явно задан только limits, то requests по дефолту будет равен ему. Если задан только requests, то limits по дефолту будет не ограничен.


## 3 
Модифицируйте свое приложение так, чтобы оно стартовало не сразу (с задержкой секунд 20-30) и падало спустя минуты работы. 

Добавьте liveness и readiness пробы , посмотрите что будет происходить.

Напишите в описании -- чего вы этим добились.

Закоммититьте отдельный манифест online-inference-pod-probes.yaml (и изменение кода приложения)

(3 балла)

Опубликуйте ваше приложение (из ДЗ 2) с тэгом v2

Добавил версии докер образа: 
 - spintowin/heart-dis:v2   - запускается, ожидает 45 секунд и падает с ошибкой (raise OSError("Application stop"))
 - spintowin/heart-dis:v3   - запускается, ожидает 45 секунд и работает

В первом случае (тэг v2) приложение падает, а livenessProbe пытается перезапустить контейнер.

Во втором случае (тэг v3) в какой-то момент приложение переходит в статус (running, ready) и в логах видно как readinessProbe постоянно шлет запросы к эндпоинту heathcheck


## 4
Создайте replicaset, сделайте 3 реплики вашего приложения. (https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

Ответьте на вопрос, что будет, если сменить докер образа в манифесте и одновременно с этим 

а) уменьшить число реплик

б) увеличить число реплик.

Поды с какими версиями образа будут внутри будут в кластере?
(3 балла)

Закоммитьте online-inference-replicaset.yaml

а) часть контейнеров перейдет в статус Completed, а версия docker образа в живых контейнерах останется первоначальный

б) появятся новые контейнеры с новой версией образа, но старые останутся без изменений


## 5 
Опишите деплоймент для вашего приложения.  (https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

Играя с параметрами деплоя (maxSurge, maxUnavaliable), добейтесь ситуации, когда при деплое новой версии 

a) Есть момент времени, когда на кластере есть как все старые поды, так и все новые (опишите эту ситуацию) (закоммититьте файл online-inference-deployment-blue-green.yaml)

б) одновременно с поднятием новых версии, гасятся старые (закоммитите файл online-inference-deployment-rolling-update.yaml)
(3 балла)

а) maxSurge: 100%, maxUnavailable: 0%

б) maxSurge: 50%, maxUnavailable: 50%


