"""Учебные задания по FastAPI."""

import uvicorn
from fastapi import FastAPI

from tasks import ws_router
from tasks import excel_router


if __name__ == '__main__':
    # Создаем приложение
    app = FastAPI(title='FastAPI test tasks',)

    # WebSocket сообщения
    app.include_router(ws_router)
    # Генерация файла Excel на лету
    app.include_router(excel_router)

    uvicorn.run('run:app', host='0.0.0.0', reload=True)
