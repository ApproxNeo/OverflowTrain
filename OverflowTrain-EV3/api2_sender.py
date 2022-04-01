import requests
import time
import sys


URL = 'http://143.198.208.163:5000/'
API = 'api/orders'


def get_new_order(retry_delay: int = 2):
    sent_waiting_message = False
    while True:
        try:
            response = requests.delete(URL + API + "/popfirst")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                if not sent_waiting_message:
                    print("Waiting for next destination...")
                    sent_waiting_message = True
            else:
                raise Exception

        except:
            print("No connection to '" + URL + "'! Try again!")

        time.sleep(retry_delay)


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.pp0
    '''

    print(*args, **kwargs, file=sys.stderr)
    print(*args)
