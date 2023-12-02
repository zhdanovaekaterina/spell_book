from src.core.instance import BaseInstance


def test_base_instance():
    """
    Тест работы базовой сущности для датаклассов
    :return:
    """

    class MyClass(BaseInstance):
        param: str = None
        param2: str = None

    obj = MyClass(param='param')  # проверяем сеттинг атрибута через конструктор
    assert hasattr(obj, 'param')

    obj.add(param2='param2')  # проверяем сеттинг через add
    assert hasattr(obj, 'param2')

    obj.add(param3='param3')  # проверяем что необъявленный атрибут не засеттится
    assert not hasattr(obj, 'param3')
