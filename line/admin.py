from django.contrib import admin

# Register your models here.
from .models import *
admin.AdminSite.site_header = "Tour CMS"
admin.AdminSite.site_title = "Tour CMS"


class TourOfferingInline(admin.TabularInline):
	model = TourOffering
	extra = 3

class TourOfferingAdmin(admin.ModelAdmin):
	search_fields = ['tour.name', 'tour.description']
	list_filter = ['offer_date']

class TourAdmin(admin.ModelAdmin):
	inlines = [TourOfferingInline]
	search_fields = ['name', 'description']	
	list_filter = ['duration', 'price']

class BookingAdmin(admin.ModelAdmin):
	search_fields = ['tourOffering.name', 'user.name']

admin.site.register(User)
admin.site.register(Tour, TourAdmin)
admin.site.register(TourOffering, TourOfferingAdmin)
admin.site.register(Booking, BookingAdmin)