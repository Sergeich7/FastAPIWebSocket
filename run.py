"""FastAPI & WebSocket.

ЗАДАЧА:
С использованием fastapi необходимо сделать веб-страницу сочетающую из:
1. Формы с текстовым полем
2. Списком сообщений пронумерованных с 1

Страница подключается к серверу по WebSocket.
С помощью формы вы можете отправить сообщение на сервер, где оно будет
принято и добавлен порядковый номер этого сообщения. Далее сообщение
с порядковым номером отправляется на страницу и отображается в списке.

При перезагрузке страницы данные о нумерации теряются и начинается с 1.

Страница должна быть динамической, обрабатывать все действия без перезагрузки.
Имеется ввиду что при отправке сообщения на сервер через вебсокет
страница не должна перезагружаться.  
Взаимодействие с сервером по вебсокет нужно реализовать с использованием JSON.
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
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('p')
                const obj = JSON.parse(event.data)
                var content = document.createTextNode(
                    obj['number'] + ' ' + obj['text'])
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify({'text': input.value}))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

message_number = 0


@app.get("/")
async def get():
    """Отдаем главную страницу."""
    global message_number
    message_number = 0
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket обработчик."""
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        global message_number
        message_number += 1
        await websocket.send_json(
            {
                "number": message_number,
                "text": data['text'],
            })
