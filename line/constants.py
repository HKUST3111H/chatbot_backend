from common.enum_type import EnumBase

import inspect
from enum import Enum

class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(p[1].value, p[0]) for p in props])
        return choices

class BookingState(ChoiceEnum):
	IS_BOOKING = 0
	DONE = 1
	CONFIRMED = 2

class TourOfferingState(ChoiceEnum):
	NOT_ENOUGH = 0
	ENOUGH = 1
	FULL = 2
	OLD = 3
