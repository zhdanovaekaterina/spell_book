from src.core import helpers


def test_snake_to_camel():
    """
    Тест преобразования строки из snake_style в CamelStyle
    :return:
    """

    input_str = 'time_to_cast'
    output_str = helpers.snake_to_camel(input_str)
    assert output_str == 'TimeToCast'
