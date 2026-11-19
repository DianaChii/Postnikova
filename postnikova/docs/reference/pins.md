---
title: Распиновка GPIO
section: Справочники
order: 1
tags: [reference, hardware]
---

# Справочник распиновки SmartSense

## Расположение пинов
┌─────────────────────┐
│  [USB-C]      [ANT] │
│                     │
│  GPIO 0  GPIO 1     │
│  GPIO 2  GPIO 3     │
│  GPIO 4  GPIO 5     │
│                     │
│  GND  VCC  3V3      │
└─────────────────────┘

## Таблица параметров

| Пин | Тип | Напряжение | Макс. ток | Функция |
|-----|-----|------------|-----------|---------|
| GPIO 0 | Digital I/O | 3.3V | 12 mA | UART TX |
| GPIO 1 | Digital I/O | 3.3V | 12 mA | UART RX |
| GPIO 2 | Digital I/O | 3.3V | 12 mA | I2C SDA |
| GPIO 3 | Digital I/O | 3.3V | 12 mA | I2C SCL |
| GPIO 4 | PWM | 3.3V | 20 mA | LED control |
| GPIO 5 | ADC | 3.3V | - | Analog input |
| VCC | Power | 5V | 500 mA | Main power |
| GND | Ground | 0V | - | Common ground |
| 3V3 | Power | 3.3V | 100 mA | Regulated output |

## Спецификации

- Рабочая температура: -20°C до +70°C
- Влажность: 10-90% без конденсации
- Питание: 3.3V - 5V DC

!!! warning "Ограничения"
    Суммарный ток всех GPIO не должен превышать 50 mA.





