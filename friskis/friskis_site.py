"""A module to handle a friskis site."""

from requests import post, get
from datetime import datetime
from .workout import Workout
import json
from .helpers import get_date_string


class FriskisSite:
    """Representation of a friskis site."""

    def __init__(self, url):
        """Init a site with the login url."""
        self.loginUrl = url + '/auth/login'
        self.activitiesUrl = url + '/businessunits/1/groupactivities?period.start='

    def login(self, username: str, password: str):
        """Login a user to a site with the given credentials."""
        credentials = {'username': username,
                       'password': password}

        response = post(self.loginUrl, json=credentials)
        if (response.status_code != 200):
            response.raise_for_status()
        return response

    def get_workouts_in_3_days(self, token):
        """Retrieve all workouts scheduled in 3 days."""
        date_string = get_date_string(2)
        url = self.activitiesUrl + date_string + '&webCategory=1'
        auth = {'Authorization': 'Bearer ' + token}
        response = get(url, json=auth)
        activities = json.loads(response.text)

        workouts = []
        for elem in activities:
            date, time = elem['duration']['start'].split('T')

            day_string = datetime.fromisoformat(date).strftime("%A")

            w = Workout(day_string, elem['name'], time[:5], workout_id=int(elem['id']))
            workouts.append(w)

        return workouts
