"""A friskis booking script."""

import time
import argparse
import requests

from friskis import FriskisSite, get_access_token, Schema, Booker, BookingError

if __name__ == '__main__':
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--site', required=True, type=str, help='The F&S site')
    parser.add_argument('--user', required=True, type=str, help='The username')
    parser.add_argument('--password', required=True, type=str, help='The password')
    parser.add_argument('--schema', required=True, type=str, help='The workout schema json file')
    args = parser.parse_args()

    site2url = {'Lidköping': 'https://fslidkoping.brpsystems.com/brponline/api/ver3'}

    site = FriskisSite(site2url[args.site])

    try:
        response = site.login(args.user, args.password)
        token = get_access_token(response.text)
        workouts_in_3_days = site.get_workouts_in_3_days(token)
        my_workouts = Schema.parse(args.schema)
        matched_workouts = [workout for workout in workouts_in_3_days if workout in my_workouts]

        if matched_workouts:
            b = Booker(site2url[args.site], token)
            for m in matched_workouts:
                status = b.book(m)
                print(f'Status: {status}')
        else:
            print('Status: Nothing to book today')


    except requests.HTTPError as e:
        print(e)
    except BookingError as e:
        print(e)

    print("--- %s seconds ---" % (time.time() - start_time))
