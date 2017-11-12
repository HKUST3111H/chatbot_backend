from django.contrib import admin
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .utils import push_message_to_users, line_multicast, line_push
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.html import format_html

# Register your models here.
from .models import *
from .forms import *
admin.AdminSite.site_header = "Tour CMS"
admin.AdminSite.site_title = "Tour CMS"


class TourOfferingInline(admin.TabularInline):
	model = TourOffering
	exclude = ['price']
	extra = 3

class BookingInline(admin.TabularInline):
	model = Booking
	exclude = ['tour_fee']
	extra = 1

@admin.register(TourOffering)
class TourOfferingAdmin(admin.ModelAdmin):

	# input is TourOffering object
	def default_offer_fee(self, obj):
		if obj.offer_date.weekday() < 5:
			return obj.tour.weekday_price
		else :
			return obj.tour.weekend_price

	# input is booking object 
	def default_tour_fee(self, booking_obj, tourOffing_obj):
		return booking_obj.adult_num * tourOffing_obj.price + 0.8 * booking_obj.child_num * tourOffing_obj.price 

	def update_price(self, request, queryset):
		rows_updated = 0
		for obj in queryset:
			if obj.price != self.default_offer_fee(obj):
				obj.price = self.default_offer_fee(obj)
				rows_updated += 1
				print (obj.price, self.default_offer_fee(obj))
				obj.save()
		if rows_updated == 1:
			message_bit = "1 tour offering was"
		else:
			message_bit = "{} tour offerings were".format(rows_updated)
		self.message_user(request, "{} successfully updated.".format(message_bit))

	def save_model(self, request, obj, form, change):
		obj.price = self.default_offer_fee(obj)
		for booking in obj.booking_set.all():
			booking.tour_fee = self.default_tour_fee(booking, obj)
			booking.save()
		obj.save()

	def tour_offering_actions(self, obj):
		return format_html(
			'<a class="" href="{}">Confirm</a>'
			'<br>'
			'<a class="" href="{}">Cancel</a>',
			reverse("admin:tour_offering_confirm", args=[obj.pk]),
			reverse("admin:tour_offering_cancel", args=[obj.pk]),
			)

	def get_urls(self):
		urls = super(TourOfferingAdmin, self).get_urls()
		custom_urls = [
			url(
				r'^(?P<tour_offering_id>\d+)/confirm/$',
				self.admin_site.admin_view(self.confirm),
				name='tour_offering_confirm',
			),
			url(
				r'^(?P<tour_offering_id>\d+)/cancel/$',
				self.admin_site.admin_view(self.cancel),
				name='tour_offering_cancel',
			),
		]
		return custom_urls + urls

	def confirm(self, request, tour_offering_id, *args, **kwargs):
		obj = self.get_object(request, tour_offering_id)
		self.message_user(request, "Successfully Confirmed.")
		message = "Your tour {} on {} is confirmed!".format(obj.tour.name, obj.offer_date.date())
		line_multicast(list(TourOffering.objects.get(pk=tour_offering_id).user.values_list('id', flat=True)), message)
		return self.changelist_view(request)
		# return HttpResponseRedirect(reverse('admin:line_tourOffering_changelist'))


	def cancel(self, request, tour_offering_id, *args, **kwargs):
		obj = self.get_object(request, tour_offering_id)
		self.message_user(request, "Successfully Canceled.")
		message = "Your tour {} on {} is canceled!".format(obj.tour.name, obj.offer_date.date())
		line_multicast(list(TourOffering.objects.get(pk=tour_offering_id).user.values_list('id', flat=True)), message)
		return self.changelist_view(request)

	tour_offering_actions.short_description = "Action"
	actions = [update_price]
	exclude = ['price']
	inlines = [BookingInline, ]
	list_display = ['tour_name', 'user_names', 'price', 'state', 'offer_date', 'available', 'tour_offering_actions']
	search_fields = ['tour__name']
	list_filter = ['offer_date']
	icon = '<i class="material-icons">event</i>'

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
	list_display = ['name', 'description', 'duration', 'weekday_price', 'weekend_price']
	inlines = [TourOfferingInline]
	search_fields = ['name', 'description']	
	list_filter = ['duration', 'weekday_price', 'weekend_price']
	icon = '<i class="material-icons">flight_takeoff</i>'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if obj.tour_fee == obj.paid_fee:
			line_push(obj.user.id, "Paymetn Confirmed")
		obj.save()

	def booking_action(self, obj):
		return format_html(
			'<a class="button" href="{}">Paid</a>&nbsp;',
			reverse('admin:booking-push_confirm_message', args=[obj.pk]),
		)

	def get_urls(self):
		urls = super(BookingAdmin, self).get_urls()
		custom_urls = [
			url(
				r'^(?P<booking_id>\d+)/push_confirm_message/$',
				self.admin_site.admin_view(self.push_confirm_message),
				name='booking-push_confirm_message',
			),
		]
		return custom_urls + urls

	def push_confirm_message(self, request, booking_id, *args, **kwargs):
		user_id = Booking.objects.get(pk=booking_id).user.pk
		line_push(user_id, "Payment Confirmed")
		self.message_user(request, "Successfully sent message to {}.".format(User.objects.get(pk=user_id).name))
		# return HttpResponseRedirect(reverse('admin:line_booking_changelist'))
		return self.changelist_view(request)

	search_fields = ['tourOffering__tour__name', 'user__name',]
	list_display = ('tour_name', 'user_name', 'booking_action', 'state')
	icon = '<i class="material-icons">archive</i>'
	booking_action.short_description = "Action"

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name', 'push_date', 'rate', 'seat', 'quota', 'available', 'will_push_recently', 'pushed', ]
	list_filter = ['push_date', 'rate', 'quota']
	icon = '<i class="material-icons">alarm</i>'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

	def push_message(self, request, queryset):

		form = None

		print (request.POST)
		if 'push' in request.POST:
			form = MessageForm(request.POST)
			if form.is_valid():
				message = form.cleaned_data['message']
				users = form.cleaned_data['users']
				# push_message_to_users(users, message)
				line_multicast(list(users.values_list('id', flat=True)), message)
				self.message_user(request, "{} message successfully send.".format(len(users)))
				return HttpResponseRedirect(request.get_full_path())

		if not form:
			form = MessageForm(initial={'message': "", 'users' :queryset})

		return render(request, "admin/user/action_push_message.html", {'users': queryset, 'form': form})
		# return render_to_response("admin/user/action_push_message.html", {'users': queryset, 'form': form})

	def recommend(self, request, queryset):
		for obj in queryset:
			print (list((TourOffering.objects.exclude(pk__in = obj.booking_set.all().filter(state=2).values_list('tourOffering__id', flat=True))).values_list('tour__name', flat=True)))
			tour_name_list = list((TourOffering.objects.exclude(pk__in = obj.booking_set.filter(state=2).values_list('tourOffering__id', flat=True))).values_list('tour__name', flat=True))
			message = "Based on your travel history, we recommend the following tours to you for your information.\n"
			for i, tour_name in enumerate(tour_name_list):
				message += "{}. {} \n".format(i, tour_name)
			# print (obj.pk, message)
			line_push(obj.pk, message)
		self.message_user(request, "{} message successfully send. ".format(len(queryset)))

	actions = [push_message, recommend]
	inlines = [BookingInline,]
	list_display = ['name', 'line_id', 'phone_num', 'state', 'last_login', 'travel_id',]
	exclude = ['id',]
	search_fields = ['id', 'name']
	list_filter = ['last_login']
	empty_value_display = '-Not filled-'
	icon = '<i class="material-icons">account_box</i>'

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
	search_fields = ['question', 'answer']
	list_filter = ['hit']
	list_display = ['question', 'answer', 'get_keyword', 'hit']
	filter_horizontal = ['keyword']
	icon = '<i class="material-icons">question_answer</i>'

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
	search_fields = ['keyword_text']
	icon = '<i class="material-icons">book</i>'

@admin.register(UserChoose)
class UserChooseAdmin(admin.ModelAdmin):
	search_fields = ['user__name']

@admin.register(UnknownQuestion)
class UnknownQuestionAdmin(admin.ModelAdmin):
	search_fields = ['question']
	icon = '<i class="material-icons"> question_answer</i>'
	list_display = ['question', 'hit']