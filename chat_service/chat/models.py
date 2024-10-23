from django.db import models

class FriendRequest(models.Model):
	class Status(models.IntegerChoices):
		PENDING = 0,
		ACCEPTED = 1,

	user_sender = models.BigIntegerField()
	user_recipient = models.BigIntegerField()
	user_sender_blocked = models.BooleanField()
	user_recipient_blocked = models.BooleanField()
	status = models.IntegerField(choices=Status)
