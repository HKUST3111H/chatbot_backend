from django.test import TestCase
import datetime
from django.utils import timezone
from .models import TourOffering

# Create your tests here.
def test_was_offered_recently_with_old_tour(self):
    """
    was_offered_recently() returns False for tour_offering whose offer_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_tour_offering = TourOffering(offer_date=time)
    self.assertIs(old_tour_offering.was_offered_recently(), False)

def test_was_offered_recently_with_recent_tour(self):
    """
    was_offered_recently() returns True for tour_offering whose offer_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_tour_offering = TourOffering(offer_date=time)
    self.assertIs(recent_tour_offering.was_offered_recently(), True)