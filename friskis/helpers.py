"""A module with some helper functions."""
import json
from datetime import datetime, timedelta
import pytz
import time


def get_access_token(text: str) -> str:
    """Get the access token."""
    body = json.loads(text)
    return body['access_token']


def get_date_string(days_in_future):
    """Get the access token."""
    now = datetime.now()
    later = now + timedelta(days=days_in_future)
    add = 'T23:00:00.000Z' if is_CET(later) else 'T22:00:00.000Z'
    return later.isoformat().split('T')[0] + add


def is_CET(day) -> int:
    """Decide if a given day is CET(+1 hour) in Stockholm. False if CEST(+2 hour)."""
    later_localized = pytz.timezone("Europe/Stockholm").localize(day)
    if later_localized.utcoffset() == timedelta(hours=1):
        return True
    else:
        return False


def wait_until_8_oclock():
    """Wait until 8 o'clock. Skip if time now is after 8 o'clock."""
    now = datetime.now()
    target = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    if target > now:
        sleep_time = (target - now).total_seconds()
        print(f'Sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)


def send_mail(subject, status, recipients, user, password):
    """Send email to user through gmail account."""
    import smtplib

    print('Sending mail')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    header = f'Subject: {subject}'
    msg = header + '\n\n ' + status
    server.sendmail(user,
                    recipients,
                    msg.encode('utf-8'))
    server.quit()
    print('Mail sent')
