
Пример структуры для хранилища данных бота

```python
data_storage = {
    'user_id': 0,
    'level': 0,
    'user_class': '',
    'user_class_properties': {
        'learn': True,
        'prepare': True
    },
    'spell_data': {
        'available': [],
        'learned': [],  # если доступно
        'prepared': [],  # если доступно
    }
}
```