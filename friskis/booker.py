"""A module to handle the booking post request."""

from requests import post
from .booking_error import BookingError
import json
from datetime import datetime
from .helpers import wait_until_8_oclock


class Booker:
    """A class for workout bookings."""

    def __init__(self, url, token):
        """Init the Booker."""
        self.url = url + '/customers/7283/bookings/groupactivities'
        self.token = token
        self.REPETITIONS = 10

    def book(self, workout):
        """Book a workout with a given id."""
        body = {'groupActivity': workout.id, 'allowWaitingList': 'true'}
        headers = {'Authorization': 'Bearer ' + self.token}

        repeat = self.REPETITIONS
        while repeat:
            repeat -= 1
            print(datetime.now())
            res = post(self.url, json=body, headers=headers)

            msg = json.loads(res.text)

            if res.status_code == 201:
                if msg['type'] == 'groupActivityBooking':
                    return "Booked"
                elif msg['type'] == 'waitingListBooking':
                    pos = msg['waitingListBooking']['waitingListPosition']
                    return f'Waiting list Pos: {pos}'
            elif res.status_code == 403:
                if msg['errorCode'] == 'TOO_EARLY_TO_BOOK':
                    wait_until_8_oclock()
                elif msg['errorCode'] == 'ALREADY_BOOKED':
                    raise (BookingError('ALREADY_BOOKED'))
            else:
                print(res.status_code, res.text)

        raise BookingError(f'Tried {self.REPETITIONS} times without success')
