"""A module for booking error exceptions."""


class BookingError(Exception):
    """A class to handle exceptions in booking."""

    def __init__(self, status):
        """Init the exception."""
        self.status = status
        super().__init__()

    def __str__(self):
        """Turn exception into printable string."""
        return f'Booking Error: {self.status}'
