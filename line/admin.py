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
	search_fields = ['tour.name', 'tour.description']
	list_filter = ['offer_date']
	filter_horizontal = ['user']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
	inlines = [TourOfferingInline]
	search_fields = ['name', 'description']	
	list_filter = ['duration', 'weekday_price', 'weekend_price']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	search_fields = ['tourOffering.name', 'user.name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	search_fields = ['id', 'name']
	list_filter = ['last_login']
