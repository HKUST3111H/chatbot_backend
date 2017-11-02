from django.db import models

import datetime
from django.utils import timezone
# Create your models here.

class User(models.Model):

	def __str__(self):
		if self.name:
			return self.name
		else:
			return ""

	id = models.CharField(max_length=50, primary_key = True)
	name = models.CharField(max_length=20, null=True)
	phone_num = models.CharField(max_length=20, null=True)
	age = models.CharField(max_length=20, null=True)
	state = models.IntegerField(default=0)	
	last_login = models.DateTimeField('login date', null=True)

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
		return self.tour.name
	
	def was_offered_recently(self):
		now = timezone.now()
		return now >= self.offer_date >= now - datetime.timedelta(days=1)

	def default_offer_time():
	    now = timezone.now()
	    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
	    return start


	def tour_name(self):
		return self.tour.name

	def get_user_name(self):
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
	state = models.IntegerField(default=0)
	price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

	was_offered_recently.admin_order_field = 'offer_date'
	was_offered_recently.boolean = True
	was_offered_recently.short_description = 'Offered recently?'

	get_user_name.allow_tags = True
	get_user_name.short_description = "User name"

class Booking(models.Model):

	def __str__(self):
		return self.tourOffering.tour.name

	def tour_name(self):
		return self.tourOffering.tour.name

	def user_name(self):
		return self.user.name

	tourOffering = models.ForeignKey(TourOffering, on_delete=models.CASCADE)
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	adult_num = models.IntegerField(default=1, null=True)
	child_num = models.IntegerField(default=0, null=True)
	toddler_num = models.IntegerField(default=0, null=True)
	tour_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=True)
	paid_fee = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=True)
	special_request = models.CharField(default="None", max_length=200, null=True)
	state = models.IntegerField(default=0)

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
