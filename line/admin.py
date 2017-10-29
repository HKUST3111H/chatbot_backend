from django.contrib import admin

# Register your models here.
from .models import *
admin.AdminSite.site_header = "Tour CMS"
admin.AdminSite.site_title = "Tour CMS"


class TourOfferingInline(admin.TabularInline):
	model = TourOffering
	extra = 3

@admin.register(TourOffering)
class TourOfferingAdmin(admin.ModelAdmin):
	list_display = ['tour_name', 'user_name', 'state', 'was_offered_recently']
	search_fields = ['tour__name']
	list_filter = ['offer_date']
	filter_horizontal = ['user']

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