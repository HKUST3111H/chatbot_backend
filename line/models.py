from django.db import models

import datetime
from django.utils import timezone
# Create your models here.

class User(models.Model):

	def __str__(self):
		return self.name

	id = models.CharField(max_length=50, primary_key = True)
	name = models.CharField(max_length=20)
	phone_num = models.CharField(max_length=20)
	age = models.CharField(max_length=20)
	state = models.IntegerField(default=0)	
	last_login = models.DateTimeField('login date', default=None)

class Tour(models.Model):

	def __str__(self):
		return self.name
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	duration = models.IntegerField(default=3)
	weekday_price = models.IntegerField(default=0)
	weekend_price = models.IntegerField(default=0)

class TourOffering(models.Model):
	
	tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
	offer_date = models.DateTimeField('offer date')
	user = models.ManyToManyField(
		User,
		through = 'Booking',
		through_fields = ('tourOffering', 'user'),
		)
	hotel = models.CharField(max_length=200)
	capacity_min = models.IntegerField(default=5)
	capacity_max = models.IntegerField(default=30)
	guide_name = models.CharField(max_length=20)
	guide_line = models.CharField(max_length=50)
	state = models.IntegerField(default=0)
	
	def was_offered_recently(self):
		now = timezone.now()
		return now >= self.offer_date >= now - datetime.timedelta(days=1)

class Booking(models.Model):
	tourOffering = models.ForeignKey(TourOffering, on_delete=models.CASCADE)
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	adult_num = models.IntegerField(default=1)
	child_num = models.IntegerField(default=0)
	elder_num = models.IntegerField(default=0)
	tour_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	paid_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2)
	special_request = models.CharField(default="None", max_length=200)
	state = models.IntegerField(default=0)

class Faq(models.Model):
	question = models.CharField(max_length=500)
	answer = models.CharField(max_length=500)
	hit = models.IntegerField(default=0)
