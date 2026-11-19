---
title: API SmartSense
section: Справочники
order: 2
tags: [reference, api]
---

# Справочник API

## Базовый URL
http://<device-ip>:8080/api/v1

## Эндпоинты

### GET /status

Получить статус устройства.

**Ответ:**

```json
{
  "status": "online",
  "uptime": 3600,
  "temperature": 42.5,
  "wifi_rssi": -65
}

POST /config
Обновить конфигурацию.
Запрос:

{
  "wifi": {
    "ssid": "MyNetwork",
    "password": "secret"
  }
}






