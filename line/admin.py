from django.contrib import admin

# Register your models here.
from .models import *
admin.AdminSite.site_header = "Tour CMS"
admin.AdminSite.site_title = "Tour CMS"


class TourOfferingInline(admin.TabularInline):
	model = TourOffering
	extra = 3

class BookingInline(admin.TabularInline):
	model = Booking
	exclude = ['tour_fee']
	extra = 1

@admin.register(TourOffering)
class TourOfferingAdmin(admin.ModelAdmin):

	# input is TourOffering obejct
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

	actions = [update_price]
	exclude = ['price']
	inlines = [BookingInline, ]
	list_display = ['tour_name', 'get_user_name', 'price', 'state', 'offer_date', 'was_offered_recently']
	search_fields = ['tour__name']
	list_filter = ['offer_date']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
	list_display = ['name', 'description', 'duration', 'weekday_price', 'weekend_price']
	inlines = [TourOfferingInline]
	search_fields = ['name', 'description']	
	list_filter = ['duration', 'weekday_price', 'weekend_price']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	search_fields = ['tourOffering__tour__name', 'user__name']
	list_display = ('tour_name', 'user_name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	inlines = [BookingInline,]
	list_display = ['name', 'id', 'state', 'last_login']
	exclude = ['id',]
	search_fields = ['id', 'name']
	list_filter = ['last_login']
	empty_value_display = '-Not filled-'

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
	search_fields = ['question', 'answer']
	list_filter = ['hit']
	list_display = ['question', 'answer', 'get_keyword', 'hit']
	filter_horizontal = ['keyword']

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
	search_fields = ['keyword_text']

@admin.register(UserChoose)
class UserChooseAdmin(admin.ModelAdmin):
	search_fields = ['user__name']