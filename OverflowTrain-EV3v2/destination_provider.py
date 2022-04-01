import requests
import time

#TODO: change to proper url
URL = "http://train.np-overflow.club/"


class DestinationProvider:
    def __init__(self):
        pass

    def get_next_destination(self, retry_delay=2):
        sent_waiting_message = False
        while True:
            try:
                response = requests.delete(URL + "api/orders/popfirst")
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
