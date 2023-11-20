from src.core.instance import BaseInstance


def test_base_instance():
    """
    Тест работы базовой сущности для датаклассов
    :return:
    """

    class MyClass(BaseInstance):
        pass

    obj = MyClass(param='param')
    assert hasattr(obj, 'param')
    assert obj.param == 'param'

    obj.add(param2='param2')
    assert hasattr(obj, 'param2')
    assert obj.param2 == 'param2'
