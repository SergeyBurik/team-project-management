import json
import random
import time

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.dispatch import receiver
from websocket import create_connection

from lamp import settings


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
	# creating user account in messenger
	ws = create_connection(settings.MESSENGER_URL)

	# send request to the websocket server
	ws.send(
		json.dumps(
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
	)

	result = json.loads(ws.recv())
	print(result)
	if result['code'] == 500:
		raise Exception(result.message)

	ws.close()


class Board(models.Model):
	PROGRAMMING = 'Programming'
	DRAWING = 'Drawing'
	MUSIC = 'Music'

	CATEGORIES = (
		(PROGRAMMING, 'Programming'),
		(DRAWING, 'Drawing'),
		(MUSIC, 'Music'),
	)

	name = models.CharField(max_length=100, verbose_name="Board's name")
	type = models.CharField(max_length=15, choices=CATEGORIES, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=100, verbose_name="Board's token",
	                         default=hash(str(name) + str(random.randint(1111111, 9999999))), unique=True)

	def save(self, *args, **kwargs):
		# creating board group chat
		ws = create_connection(settings.MESSENGER_URL)
		# send request
		ws.send(
			json.dumps(
				{
					"action": "create_group",
					"from_user": self.author.username,
					"group_id": self.token,
					"users": [self.author.username],
					"time": time.time()
				}
			)
		)

		result = json.loads(ws.recv())
		if result['code'] == 500:
			raise Exception(result.message)

		ws.close()
		super(Board, self).save(*args, **kwargs)


"""
from mixer.backend.django import mixer
from mainapp.models import Board
from mainapp.models import Teammate
from mainapp.models import Column
mixer.blend(Board)

"""


class Column(models.Model):
	name = models.CharField(max_length=100, verbose_name="Column's name")
	board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Task(models.Model):
	name = models.CharField(max_length=100, verbose_name="Board's name")
	description = models.TextField(max_length=500)
	column = models.ForeignKey(Column, on_delete=models.CASCADE)


class Image(models.Model):
	image = models.ImageField(verbose_name="Task's image")
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Mark(models.Model):
	name = models.CharField(max_length=100, verbose_name="Mark's name")
	colour = models.CharField(max_length=50, verbose_name="Mark's colour")
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskParticipate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Teammate(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		# adding new teammate group chat
		ws = create_connection(settings.MESSENGER_URL)
		# send request
		ws.send(json.dumps({"action": "add_user_to_group",
		                    "from_user": self.user.username,
		                    "group_id": self.board.token,
		                    "time": time.time()}))

		result = json.loads(ws.recv())
		if result['code'] == 500:
			raise Exception(result.message)

		ws.close()
		super(Teammate, self).save(*args, **kwargs)
