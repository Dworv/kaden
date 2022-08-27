from json import load


def read_config(*fields: list[str]) -> str | int | float | dict | list:
    """
    Reads a field from the config file.

    Use a different arg for each nested field name.
    """
    with open("config.json") as f:
        item: dict = load(f)
        for field in fields:
            item = item.get(field)
        return item
