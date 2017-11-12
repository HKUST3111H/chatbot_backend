from django.core.management.base import BaseCommand, CommandError
from line.models import*
import datetime
from django.utils import timezone
from line.utils import *

class Command(BaseCommand):
    help = 'Check whether the discount is pushed'

    def add_arguments(self, parser):
        parser.add_argument('--minutes', default=5, type=int)

    def handle(self, *args, **options):
    	now = timezone.now()
    	delta = datetime.timedelta(minutes=options['minutes'])
    	discounts = Discount.objects.filter(pushed=False).filter(push_date__range= [now - delta, now + delta])
    	message = "We are offering following discount!\n\n"
    	for discount in discounts:
    		message += "{}\n{}\n".format(discount.name, discount.tourOffering.tour_name)
    		message += "Only {} quota!".format(discount.quota)
    		discount.pushed = True
    		discount.save()
    	message += "Act now to book at the discount price!"
    	print (message)
    	if len(discounts):
    		print ("sent!")
	    	line_multicast(list(User.objects.all().values_list('id', flat=True)), message)
    	self.stdout.write(self.style.SUCCESS(str(discounts)))