# Generator (service)

> Генератор будет оформлен ввиде отдельного сервиса в **Docker Compose**.  
> Основным предназначением будет являться потоковая запись в **Apache Kafka**.

## Параметры

Параметр | Значение | Статус
-|-|-
**Тип записи в Apache Kafka** | ассинхронный | `нереализовано`
**Максимальное количество Topic'ов** | 7 | `нереализовано`
**Время работы генератора** | 4 минуты | `нереализовано`
**Формат сообщений** | `json` | `нереализовано`
**Режим запуска** | одиночный | `нереализовано`
**Схема сообщений** | единая с вариативным `payload` | `нереализовано`

## Source Information

### Топики

1. `item_liked` - товар понравился (не корзина)
2. `item_ordered` - товар заказали
3. `item_clicked` - по товару перешли
4. `item_rated` - товар оценили
5. `item_viewed` - товар был просмотрен
6. `item_reported` - на товар пожаловались
7. `item_saved` - товар поместили в корзину

### Schema

> Схема данных одна на все топики, единственное что меняется индивидуальные данные в поле `payload`

```json
{
  "event_id": "evt_3a7b...",
  "event_type": "item_viewed",
  "timestamp": "2026-07-05T12:00:00Z",
  "payload": {
    "user_id": 42,
    "item_id": 771,
    "category": "electronics",
    "price": 1299.99,
    "rating": null
  }
}
```

#### Описание

- `event_id` — UUID, уникальный для каждого события
- `event_type` — совпадает с названием топика
- `timestamp` — время генерации события, ISO 8601
- `payload` — зависит от типа события:
  - `item_rated` содержит `rating` (1-5)
  - `item_ordered` содержит `price` и `quantity`
  - `item_clicked`, `item_viewed`, `item_saved`, `item_liked` — без `rating`
  - `item_reported` содержит `reason` (string) и `category` (enum: `spam`, `inappropriate`, `counterfeit`, `defective`, `misleading`, `prohibited`)