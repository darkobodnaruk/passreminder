from django.db import models

class User(models.Model):
	email = models.CharField(max_length=100)
	confirmed = models.BooleanField(default=False)
	created_dt = models.DateTimeField(auto_now_add=True)
	updated_dt = models.DateTimeField(auto_now=True)

class PassHash(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	hashtype = models.CharField(max_length=100)
	hhash = models.CharField(max_length=200)
	created_dt = models.DateTimeField(auto_now_add=True)

class Reminder(models.Model):
	passhash = models.ForeignKey(PassHash)
	event_dt = models.DateTimeField()
	sent_dt = models.DateTimeField()
	responded_dt = models.DateTimeField()

class PassTest(models.Model):
	passhash = models.ForeignKey(PassHash)
	reminder = models.ForeignKey(Reminder)
	attempted_dt = models.DateTimeField(auto_now_add=True)
	num_attempts = models.IntegerField()
	successful = models.BooleanField()