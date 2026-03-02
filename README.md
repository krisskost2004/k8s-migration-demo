# Миграция с Docker Swarm на Kubernetes: Асинхронный пайплайн микросервисов
Тестовое задание представляет собой миграцию устаревшего решения с Docker Swarm на современный Kubernetes. В продакшене существует цепочка из 4 микросервисов (App1 → App2 → App3 → App4), которые общаются асинхронно через очередь сообщений (Message Broker).
## Содержание

Цепочка из 4 микросервисов (App1 → App2 → App3 → App4), общающихся асинхронно через NATS. Сообщение `{"message": "hello, world"}` проходит через все сервисы и фиксируется в логах.

### Поток данных

1. Пользователь отправляет JSON `{"message": "hello, world"}` в топик `app1.input`
2. **App1** получает сообщение, логирует его и пересылает в `app2.input`
3. **App2** получает сообщение, логирует его и пересылает в `app3.input`
4. **App3** получает сообщение, логирует его и пересылает в `app4.input`
5. **App4** получает сообщение, логирует его и публикует в финальный топик `app4.output`
6. Успешная обработка фиксируется в логах App4 и в топике `app4.output`
## Инструкция по запуску

### Поднять кластер

```bash
# Запуск Minikube
minikube start --driver=docker --cpus=2 --memory=4096

# Собрать образ приложения
docker build -t messaging-app:latest .

# Развернуть все компоненты
kubectl apply -f k8s/

# Проверить, что все поды запущены
kubectl get pods -n messaging-pipeline -w

# Отправить первое сообщение
kubectl apply -f k8s/05-sender-job-natsbox.yaml

# Результат в логах пода app4
kubectl logs -n messaging-pipeline -l component=app4 --tail=20

# Посмотреть результат
cat final_results.txt
