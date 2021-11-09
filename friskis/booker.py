"""A module to handle the booking post request."""

from requests import post
from .booking_error import BookingError
import json
from datetime import datetime
from .helpers import wait_until_8_oclock


class Booker:
    """A class for workout bookings."""

    def __init__(self, url, customer_id, token):
        """Init the Booker."""
        self.url = f'{url}/customers/{customer_id}/bookings/groupactivities'
        self.token = token
        self.REPETITIONS = 12

    def book(self, workout):
        """Book a workout with a given id."""
        body = {'groupActivity': workout.id, 'allowWaitingList': 'true'}
        headers = {'Authorization': 'Bearer ' + self.token}

        repeat = self.REPETITIONS
        while repeat:
            repeat -= 1
            now = datetime.now()
            print(now)
            res = post(self.url, json=body, headers=headers)

            msg = json.loads(res.text)

            if res.status_code == 201:  # Booking OK
                if msg['type'] == 'groupActivityBooking':
                    return f'Booked at {now} after {self.REPETITIONS - repeat} tries'
                elif msg['type'] == 'waitingListBooking':
                    pos = msg['waitingListBooking']['waitingListPosition']
                    return f'Waiting list Pos: {pos} at {now} after {self.REPETITIONS - repeat} tries'
            elif res.status_code == 403:
                if msg['errorCode'] == 'TOO_EARLY_TO_BOOK':
                    wait_until_8_oclock()
                elif msg['errorCode'] == 'ALREADY_BOOKED' \
                        or msg['errorCode'] == 'ALREADY_ON_WAITING_LIST' \
                        or msg['errorCode'] == 'BOOKING_CLASHES_WITH_OTHER_BOOKING':
                    raise (BookingError(msg['errorCode'] + " " + str(workout)))

        raise BookingError(f'Tried {self.REPETITIONS} times without success')
