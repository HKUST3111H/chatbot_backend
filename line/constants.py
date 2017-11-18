import inspect
from enum import Enum

class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not inspect.isroutine(m))
        # filter down to just properties
        props = [m for m in members if not m[0][:2] == '__']
        # format into django choice tuple
        choices = tuple([(p[1].value, p[0]) for p in props])
        return choices

class BookingState(ChoiceEnum):
    IS_BOOKING = 0
    CONFIRMED = 1
    PAID = 2

class TourOfferingState(ChoiceEnum):
    OPEN = 0
    CONFIRMED = 1
    CANCELED = 2
    CLOSED = 3
