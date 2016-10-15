from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	
class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=400)
	time = models.DateTimeField()