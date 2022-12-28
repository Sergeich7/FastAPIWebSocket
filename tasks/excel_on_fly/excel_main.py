"""Генерация Excel файла на лету.

В рамках решения необходимо реализовать HTTP API для генерации Excel файла
на лету. Генерация на лету означает отсутствие временных файлов,
все процедуры должны происходить в памяти.

Excel таблица должна содержать колонки:
Дата; Время; Случайное число; Случайная строка.

Значение для колонок:
текущая дата по временной зоне UTC;
текущее время по временной зоне UTC;
случайное число от 0 до 1000;
случайная строка от 2 до 12 символов. Строка должна содержать только
латинские символы в любом регистре и числа.

Первая строка Excel таблицы должна содержать наименование колонок.

К внешнему виду и форматирования нет ограничений, на усмотрение исполнителя.

Из API файл должен вернуться с mime type Excel таблицы, его имя должно
соответствовать шаблону  “file_generated_at_YYYYMMDD.xlsx”, где:
YYYY - текущий год;
MM - текущий месяц с ведущим нулем;
DD - текущий день с ведущим нулем.

Стек технологий:
FastAPI последней версии;
xlsxwriter, openpyxl - любой из перечисленных
стандартная библиотека Python.
Другие сторонние библиотеки запрещены.
"""

import io
import datetime
import random
import string

from openpyxl import Workbook

from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from fastapi import status

import settings

TASK_PREFIX = '/excel'

excel_router = APIRouter(prefix=settings.API_PREFIX + TASK_PREFIX)


@excel_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Success"},
    }
)
async def get_file():
    """Генерим на лету файлик excel."""
    # Заполняем файл
    excel_file = Workbook()
    excel_sheet = excel_file.active
    excel_sheet['A1'].value = 'Дата'
    excel_sheet['B1'].value = 'Время'
    excel_sheet['C1'].value = 'Случайное число'
    excel_sheet['D1'].value = 'Случайная строка'

    excel_sheet['A2'].value = datetime.date.today()
    excel_sheet['B2'].value = datetime.datetime.now().time()
    excel_sheet['C2'].value = random.randint(0, 1000)
    excel_sheet['D2'].value = ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for _ in range(random.randint(2, 12))
        )

    # Сохраняем файл в поток
    output = io.BytesIO()
    excel_file.save(output)
    output.seek(0)

    fn = f'file_generated_at_{datetime.date.today().strftime("%Y%m%d")}.xlsx'
    headers = {
        'Content-Disposition': f'attachment; filename="{fn}"',
    }
    return StreamingResponse(output, headers=headers)
