"""A module for handling of a workout."""


class Workout:
    """A model for a workout."""

    def __init__(self, day: str, name: str, time: str, workout_id: int = 0):
        """Init a workout with day, name, time."""
        self.day = day.lower()
        self.name = name.lower()
        self.time = time
        self.id = workout_id

    def __eq__(self, other):
        """Compare two workouts for equality.

        :type other: Workout
        """
        if (self.time == other.time
                and self.name.split(' ')[0] == other.name.split(' ')[0]
                and self.day == other.day):
            return True
        return False

    def __ne__(self, other):
        """Compare two workouts for inequality.

        :type other: Workout
        """
        return not self.__eq__(other)

    def __str__(self):
        """Represent the workout as a string."""
        return f'{self.name} on {self.day} at {self.time}'
