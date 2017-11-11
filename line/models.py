from django.db import models

import datetime
from django.utils import timezone
from .constants import *
# Create your models here.

class User(models.Model):

	def __str__(self):
		if self.name:
			return self.name
		else:
			return ""

	def line_id(self):
		return self.id

	def travel_id(self):
		return self.travel_id

	id = models.CharField(max_length=50, primary_key = True)
	name = models.CharField(max_length=20, null=True)
	phone_num = models.CharField(max_length=20, null=True)
	age = models.CharField(max_length=20, null=True)
	state = models.IntegerField(default=0)	
	last_login = models.DateTimeField('login date', null=True)
	travel_id = models.CharField(max_length=20, null=True)

	line_id.admin_order_field = 'id'
	line_id.short_description = 'Line ID'

	travel_id.admin_order_field = 'travel_id'
	travel_id.short_description = 'Travel ID'

class Tour(models.Model):

	def __str__(self):
		return self.name

	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	duration = models.IntegerField(default=3)
	weekday_price = models.IntegerField(default=0)
	weekend_price = models.IntegerField(default=0)

class TourOffering(models.Model):

	def __str__(self):
		return self.tour_name
	
	def was_offered_recently(self):
		now = timezone.now()
		return self.offer_date >= now - datetime.timedelta(days=3)

	def default_offer_time():
	    now = timezone.now()
	    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
	    return start

	@property
	def tour_name(self):
		return self.tour.name + " " + str(self.id)

	def user_names(self):
		return "<br>".join([user.name for user in self.user.all() if user.name is not None])

	tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
	offer_date = models.DateTimeField('offer date', default=default_offer_time)
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
	state = models.IntegerField(default=0, choices=TourOfferingState.VALUE_TO_NAME.items())
	price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	was_offered_recently.admin_order_field = 'offer_date'
	was_offered_recently.boolean = True
	was_offered_recently.short_description = 'Offered recently?'

	user_names.allow_tags = True
	user_names.short_description = "User name"

class Discount(models.Model):

	def __str__(self):
		return self.name

	def default_push_date():
		now = timezone.now()
		timezone.now()+datetime.timedelta(days=7)

	def available(self):
		return self.quota - len(self.tourOffering.user.all())

	def will_push_recently(self):
		now = timezone.now()
		return now + datetime.timedelta(days=3) > self.push_date > now

	name = models.CharField(max_length=50)	
	tourOffering = models.ForeignKey(TourOffering, on_delete=models.CASCADE)
	push_date = models.DateTimeField('push_date', default=default_push_date)
	rate = models.DecimalField(default=0.8, max_digits=3, decimal_places=2)
	seat = models.IntegerField(default=2)
	quota = models.IntegerField(default=4)
	pushed = models.BooleanField(default=False)

	will_push_recently.admin_order_field = 'push_date'
	will_push_recently.boolean = True
	will_push_recently.short_description = 'Pushing recently?'

class Booking(models.Model):

	def __str__(self):
		return self.tour_name

	@property
	def tour_name(self):
		return self.tourOffering.tour_name

	@property
	def user_name(self):
		return self.user.name

	tourOffering = models.ForeignKey(TourOffering, on_delete=models.CASCADE)
	discount = models.ForeignKey(Discount, null = True, on_delete=models.SET_NULL)
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	adult_num = models.IntegerField(default=1, null=True)
	child_num = models.IntegerField(default=0, null=True)
	toddler_num = models.IntegerField(default=0, null=True)
	tour_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=True)
	paid_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=True)
	special_request = models.CharField(default="None", max_length=200, null=True)
	state = models.IntegerField(default=0, choices=BookingState.VALUE_TO_NAME.items())

class UserChoose(models.Model):
	def __str__(self):
		return self.user.name

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tour_id = models.CharField(max_length=20)

class Keyword(models.Model):

	def __str__(self):
		return self.keyword_text

	keyword_text = models.CharField(max_length=20)

class Faq(models.Model):

	def __str__(self):
		return self.question

	def get_keyword(self):
		return "<br>".join([k.keyword_text for k in self.keyword.all()])

	question = models.CharField(max_length=500)
	answer = models.CharField(max_length=500)
	hit = models.IntegerField(default=0)
	keyword = models.ManyToManyField(Keyword)

	get_keyword.allow_tags = True
	get_keyword.short_description = "Keyword"

class UnknownQuestion(models.Model):

	def __str__(self):
		return self.question

	question = models.CharField(max_length=500)
	hit = models.IntegerField(default=0)
