import prettytable as pt
from aiogram import types
from config import COLUMNS_NAME


def make_table(message: types.Message, data: dict, columns_name: list) -> str:
    table = pt.PrettyTable(columns_name)
    isFirst = True

    for column_name in columns_name:
        table.align[column_name] = "r"
        if isFirst:
            table.align[column_name] = "l"
            isFirst = False

    for item in data:
        table.add_row(
            [item[COLUMNS_NAME[i]] for i in columns_name]
        )

    return table
