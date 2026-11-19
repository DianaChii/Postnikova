---
title: Настройка Wi-Fi
section: Руководства
order: 2
tags: [how-to, wifi]
---

# Как настроить Wi-Fi подключение

## Проблема

Устройство SmartSense должно подключаться к Wi-Fi сети для передачи телеметрии.

## Решение

### Шаг 1. Откройте конфиг

```bash
nano /etc/smartsense/wifi.conf

### Шаг 2. Введите данные сети

```ini
[wifi]
ssid = YourNetworkName
password = YourPassword
security = WPA2

### Шаг 3. Перезапустите устройство

```bash
sudo systemctl restart smartsense

### Шаг 4. Проверьте подключение

```bash
smartsense status --wifi

Должно появиться: WiFi: connected (192.168.1.100)



