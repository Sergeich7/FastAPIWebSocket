"""FastAPI & WebSocket.

ЗАДАЧА:
С использованием FastAPI необходимо сделать веб-страницу сочетающую из:
1. Формы с текстовым полем
2. Списком сообщений пронумерованных с 1

Страница подключается к серверу по WebSocket.
С помощью формы вы можете отправить сообщение на сервер, где оно будет
принято и добавлен порядковый номер этого сообщения. Далее сообщение
с порядковым номером отправляется на страницу и отображается в списке.

При перезагрузке страницы данные о нумерации теряются и начинается с 1.

Страница должна быть динамической, обрабатывать все действия без перезагрузки.
Имеется ввиду что при отправке сообщения на сервер через WebSocket
страница не должна перезагружаться.
Взаимодействие с сервером по WebSocket нужно реализовать с использованием JSON.
Формат и именование полей не важно. можно использовать любые.
"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html lang="ru">
<html>
    <head>
        <title>FastAPI & WebSocket</title>
    </head>
    <body>
        <h1>FastAPI & WebSocket</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <div id='messages'>
        </div>
        <script>
            var clientID = Date.now();
            var ws = new WebSocket('ws://' + document.domain + ':8000/ws');
            ws.onmessage = function(event) {
                const obj = JSON.parse(event.data)
                var content = document.createTextNode(
                    obj['number'] + ' ' + obj['text'])

                var message = document.createElement('p')
                message.appendChild(content)

                var messages = document.getElementById('messages')
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify(
                    {
                        'id': clientID,
                        'text': input.value
                    }))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    """Отдаем главную страницу."""
    return HTMLResponse(html)


def make_counter() -> int:
    """Замыкание для увеличения и хранения номера сообщения."""
    number = 0

    def incr() -> int:
        nonlocal number
        number += 1
        return number

    return incr


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket обработчик."""
    await websocket.accept()
    number_by_id = {}
    while True:
        data = await websocket.receive_json()
        client_id = data['id']

        if client_id not in number_by_id.keys():
            # Создаем счетчик для каждого клиента
            # Значение счетчика храним в замыкании
            number_by_id[client_id] = make_counter()

        # получаем номер текущего сообщения из замыкания
        message_number = number_by_id[client_id]()

        await websocket.send_json(
            {
                "number": message_number,
                "text": data['text'],
            })
