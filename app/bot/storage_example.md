
Пример структуры для хранилища данных бота

```python
data_storage = {
    'user_id': 0,
    'level': 0,
    'user_class': '',
    'user_class_action': SpellAction.BOTH,  # доступные действия для класса
    'spell_data': {},  # список заклинаний, с которым работаем
    'spell_page_count': 0  # кол-во страниц
}
```
