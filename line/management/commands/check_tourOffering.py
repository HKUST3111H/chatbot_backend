from django.core.management.base import BaseCommand, CommandError
from line.models import*
import datetime
from django.utils import timezone
from line.utils import *
from line.constants import *

class Command(BaseCommand):
	help = 'Check whether a tourOffering should be confirmed or canceled'

	def add_arguments(self, parser):
		parser.add_argument('--days', default=2, type=int)

	def handle(self, *args, **options):
		now = timezone.now()
		delta = datetime.timedelta(days=options['days'])
		tourOfferings = TourOffering.objects.filter(state = (TourOfferingState.OPEN.value)).filter(offer_date__range = [now, now + delta])
		for tourOffering in tourOfferings:
			message = ""
			if tourOffering.paid_total_num > tourOffering.capacity_min:
				tourOffering.state = TourOfferingState.CONFIRMED.value
				message = "Your tour {} on {} is confirmed!\n".format(tourOffering.tour_name, tourOffering.offer_date.date())
				message += "Please contact your tour guide {} by Line {}.".format(tourOffering.guide_name, tourOffering.guide_line)

			else :
				tourOffering.state = TourOfferingState.CANCELED.value
				message = "Your tour {} on {} is canceled!\n".format(tourOffering.tour_name, tourOffering.offer_date.date())
				message += "The minimum requirement is {} but only {} people booked. We are sorry.".format(tourOffering.capacity_min, tourOffering.total_num)
			tourOffering.save()
			line_multicast(list(tourOffering.user.all().values_list('id', flat=True)), message)
		self.stdout.write(self.style.SUCCESS(str(tourOfferings)))
		tourOfferings = TourOffering.objects.filter(offer_date__lte = now)

		tourOfferings.update(state = TourOfferingState.CLOSED.value)

		self.stdout.write(self.style.SUCCESS(str(tourOfferings)))
