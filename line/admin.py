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
	extra = 1

@admin.register(TourOffering)
class TourOfferingAdmin(admin.ModelAdmin):

	def update_price(self, request, queryset):
		rows_updated = 0
		def default_offer_fee(obj):
			if obj.offer_date.weekday() < 5:
				return obj.tour.weekday_price
			else :
				return obj.tour.weekend_price
		for obj in queryset:
			obj.price = default_offer_fee(obj)
			rows_updated += 1
			print (obj.price, default_offer_fee(obj))
			obj.save()
		if rows_updated == 1:
			message_bit = "1 tour offering was"
		else:
			message_bit = "{} tour offerings were".format(rows_updated)
		self.message_user(request, "{} successfully updated.".format(message_bit))
	actions = [update_price]
	inlines = [BookingInline, ]
	list_display = ['tour_name', 'get_user_name', 'price', 'state', 'was_offered_recently']
	search_fields = ['tour__name']
	list_filter = ['offer_date']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
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