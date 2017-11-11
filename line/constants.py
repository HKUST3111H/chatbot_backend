from common.enum_type import EnumBase

class BookingState(EnumBase):
	IS_BOOKING = 0
	DONE = 1
	CONFIRMED = 2
	VALUE_TO_NAME = {
	0: 'is booking',
	1: 'done',
	2: 'confirmed',
	}

class TourOfferingState(EnumBase):
	NOT_ENOUGH = 0
	ENOUGH = 1
	FULL = 2
	OLD = 3
	VALUE_TO_NAME = {
	0: 'not enough',
	1: 'enough',
	2: 'done',
	3: 'old',
	}



