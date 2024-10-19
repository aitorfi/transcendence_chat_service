# game/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

connected_users = {}

class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		print("Client connected")
		await self.accept()

	async def disconnect(self, close_code):
		if self.user_id:
			connected_users.pop(self.user_id)
		print("Client disconnected")

	async def receive(self, text_data):
		data = json.loads(text_data)
		message_type = data.get('type', 0)

		if message_type == 'connect':
			await self.handle_action_connect(data)
		elif message_type == 'send_message':
			await self.handle_action_send_message(data)
		else:
			await self.send(text_data=json.dumps({
				'type': 'error',
				'message': "Bad request, parameter 'type' is mandatory"
			}))

	async def handle_action_connect(self, data):
		self.user_id = data.get('user_id', 0)

		if self.user_id == 0:
			await self.send(text_data=json.dumps({
				'type': 'error',
				'message': "Bad request, parameter 'user_id' is mandatory"
			}))
		
		connected_users[self.user_id] = self
		print(f"Client {self.user_id} ready to receive messages")
	
	async def handle_action_send_message(self, data):
		if not await self.validate_data_on_action_send_message(data):
			return
		print("handle_action_send_message")
		recipient_user_id = data.get('recipient', 0)
		message = data.get('message', 0)
		
		if await self.is_valid_message(self.user_id, recipient_user_id):
			# TODO: Insertar el mensaje en la base de datos
			if recipient_user_id in connected_users:
				print(f"Enviando mensaje al usuario {recipient_user_id}")
				await connected_users[recipient_user_id].send(text_data=json.dumps({
					'type': 'incoming_message',
					'message': message
				}))
			else:
				print('The recipient user is not currently connected.')
		else:
			await self.send_error_response(f"Communication with user {recipient_user_id} is not possible.")
		
	async def validate_data_on_action_send_message(self, data):
		ret = True;
		if 'recipient' not in data:
			ret = False
			await self.send_error_response("Bad request, parameter 'recipient' is mandatory")

		if 'message' not in data:
			ret =  False
			await self.send_error_response("Bad request, parameter 'message' is mandatory")
		if ret:
			print("mensaje valido")
		else:
			print("mensaje invalido")
		return ret

	async def is_valid_message(self, sender_user_id, recipient_user_id):
		# TODO: Validar si el usuario que envía (sender_user_id) y el usuario
		# TODO: receptor (recipient_user_id) son amigos y no están bloqueados
		return True
	
	async def send_error_response(self, error_message):
		await self.send(text_data=json.dumps({
			'type': 'error',
			'message': error_message
		}))
