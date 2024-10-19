# Testeo

Para lanzar el servidor usar el siguiente comando:

```bash
daphne -p 50002 chat_service.asgi:application
```

Para probar el chat se puede usar el siguiente html pero no lo subais al repo:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Test</title>
</head>
<body>
	<style>
		table {
			width: 300px;
			border: 1px solid black;
		}
		/* .sended-message {
			text-align: right;
			
		} */
		.sended-message div {
			align-self: right;
			margin-left: auto;
			background-color: lightgreen;
		}
		/* .received-message {
			text-align: left;
		} */
		.received-message div {
			align-self: left;
			margin-right: auto;
			background-color: lightblue;
		}
		.received-message div, .sended-message div {
			border-radius: 25px;
			padding: 10px;
			width: fit-content;
		}
	</style>
    <h1>WebSocket Pong Game</h1>
		<div style="width:100%">
			<label for="user_id_txt_field">Usuario Actual</label>
			<input type="text" id="user_id_txt_field">
			<button id="connect">Connect</button>
		</div>
		<div style="width:100%; margin-top:10px">
			<label for="recipient_user_id_txt_field">Receptor</label>
			<input type="text" id="recipient_user_id_txt_field">
		</div>
		<div style="width:100%; margin-top:10px">
			<table>
				<tbody id="chat"></tbody>
			</table>
		</div>
		<div style="width:100%; margin-top:10px">
			<input type="text" id="message">
			<button id="send_message">Send Message</button>
		</div>
		
    <script>
        const socket = new WebSocket('ws://localhost:50002/ws/chat/');

        socket.onopen = function(e) {
            console.log("Conectado al WebSocket");
        };

        socket.onmessage = function(event) {
					const eventData = JSON.parse(event.data);
					if (eventData.type == "incoming_message") {
						message = eventData.message;

						chatTable = document.getElementById('chat');
						chatTable.innerHTML += 
							"<tr><td class=\"received-message\"><div>" + message + "</div></td></tr>";
					} else {
						console.log("Mensaje del servidor:", eventData);
					}
        };

        socket.onclose = function(event) {
            if (event.wasClean) {
                console.log(`Conexión cerrada limpiamente, código: ${event.code}, motivo: ${event.reason}`);
            } else {
                console.log("Conexión terminada");
            }
        };

        socket.onerror = function(error) {
            console.log("Error en el WebSocket", error);
        };

				document.getElementById("connect").onclick = () => {
						user_id = document.getElementById('user_id_txt_field').value;
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
									type: "connect",
									user_id: user_id
								}));
            }
        };

        document.getElementById("send_message").onclick = () => {
					message = document.getElementById('message').value;
					recipient = document.getElementById('recipient_user_id_txt_field').value;

					if (socket.readyState === WebSocket.OPEN) {
							socket.send(JSON.stringify({
								type: "send_message",
								message: message,
								recipient: recipient
							}));
					}

					chatTable = document.getElementById('chat');
					chatTable.innerHTML += 
						"<tr><td class=\"sended-message\"><div>" + message + "</div></td></tr>";
        };
    </script>
</body>
</html>
```