async def mock_get(self, url):
    """
    Замена методу async Parser.get()
    :return:
    """
    with open(url, 'r', encoding='utf-8') as file:
        return file.read()
