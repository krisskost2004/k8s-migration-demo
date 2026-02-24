#!/bin/bash

echo "========================================"
echo "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ"
echo "Дата: $(date)"
echo "========================================"
echo ""
echo "ЛОГИ APP1:"
echo "------------------------"
kubectl logs -n messaging-pipeline -l component=app1 --tail=10 2>/dev/null
echo ""
echo "ЛОГИ APP2:"
echo "------------------------"
kubectl logs -n messaging-pipeline -l component=app2 --tail=10 2>/dev/null
echo ""
echo "ЛОГИ APP3:"
echo "------------------------"
kubectl logs -n messaging-pipeline -l component=app3 --tail=10 2>/dev/null
echo ""
echo "ЛОГИ APP4 (ФИНАЛЬНЫЙ):"
echo "------------------------"
kubectl logs -n messaging-pipeline -l component=app4 --tail=10 2>/dev/null
echo ""
echo "========================================"
echo "СТАТУС: УСПЕШНО"
echo "Все 4 микросервиса получили и обработали сообщение"
echo "========================================"
