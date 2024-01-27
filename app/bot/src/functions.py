from math import ceil


# ############# ПАГИНАЦИЯ ##############

def get_page_count(some_list: list, per_page: int) -> int:
    """
    Получение кол-ва страниц, на которые разобьется список
    """
    return ceil(len(some_list) / per_page)


def slice_list(some_list: list, curr_page: int, per_page: int) -> list:
    """
    Получение среза списка для нужной страницы
    """

    start = (curr_page-1) * per_page
    end = start + per_page
    return some_list[start:end]
