"""A module to parse a schema file with weekly training workouts."""

import json
from datetime import datetime, timedelta
from pytz import timezone
from .workout import Workout
from .helpers import is_CET


class Schema:
    """A class to parse a workout schema file."""

    workouts = []

    @classmethod
    def parse(cls, plan):
        """Parse a json schema file."""
        with open(plan, 'r', encoding='utf8') as infile:
            data = json.load(infile)

        for e in data:
            # Convert time to UTC (from CEST/CET with correct DST handling)
            diff = 1 if is_CET(datetime.now() + timedelta(days=2)) else 2

            h, m = e['time'].split(':')
            hour = int(h) - diff
            if hour < 10:
                hour = '0' + str(hour)
            else:
                hour = str(hour)
            time = hour + ':' + m
            w = Workout(e['day'], e['name'], time)
            cls.workouts.append(w)
        return cls.workouts

    def __str__(self):
        """Define a string representation of a schema file."""
        return '\n'.join([str(w) for w in self.workouts])
