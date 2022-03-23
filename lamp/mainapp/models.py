import json
import random
import time
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from websocket import create_connection
from lamp import settings
import constants
import utils


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
	# create user account in messenger service
	utils.websocket_send(
		{
			"action": "presence",
			"username": instance.username,
			"name": {
				"first_name": instance.first_name,
				"last_name": instance.last_name
			},
			"password": instance.password,
			"time": time.time()
		}
	)


# project board model
class Board(models.Model):
	name = models.CharField(max_length=100, verbose_name="Board's name")
	type = models.CharField(max_length=15, choices=constants.CATEGORIES, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(
		max_length=100, verbose_name="Board's token",
		default=hash(str(name) + str(random.randint(1111111, 9999999))), unique=True
	)

	def save(self, *args, **kwargs):
		# creating board group chat
		utils.websocket_send(
			{
				"action": "create_group",
				"from_user": self.author.username,
				"group_id": self.token,
				"users": [self.author.username],
				"time": time.time()
			}
		)

		super(Board, self).save(*args, **kwargs)


# project board column model
class Column(models.Model):
	name = models.CharField(max_length=100, verbose_name="Column's name")
	board = models.ForeignKey(Board, on_delete=models.CASCADE)


# column task model
class Task(models.Model):
	name = models.CharField(max_length=100, verbose_name="Board's name")
	description = models.TextField(max_length=500)
	column = models.ForeignKey(Column, on_delete=models.CASCADE)


# task image model
class Image(models.Model):
	image = models.ImageField(verbose_name="Task's image")
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


# task mark model
class Mark(models.Model):
	name = models.CharField(max_length=100, verbose_name="Mark's name")
	colour = models.CharField(max_length=50, verbose_name="Mark's colour")
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


# responsible for task model
class TaskParticipate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


# teammate model (many-to-one)
class Teammate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		# adding new teammate group chat
		ws = create_connection(settings.MESSENGER_URL)
		# send request
		ws.send(
			json.dumps(
				{
					"action": "add_user_to_group",
					"from_user": self.user.username,
					"group_id": self.board.token,
					"time": time.time()
				}
			)
		)

		result = json.loads(ws.recv())
		if result['code'] == 500:
			raise Exception(result.message)

		ws.close()
		super(Teammate, self).save(*args, **kwargs)
