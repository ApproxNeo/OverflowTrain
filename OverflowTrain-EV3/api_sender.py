#from ev3dev.ev3 import *
import requests
import json
import sys
import time
import os

url = 'https://npsigfiesta.firebaseio.com/'


def get_new_order():
    access = '/orders'
    orders = None

    while orders == None:
        try:
            content = requests.get(
                url + access + '/.json', verify=False).content
            orders = json.loads(content.decode("ascii"))

            if orders != None:
                current = next(iter(orders))
                orders[current]["id"] = current
            else:
                debug_print("No order to fulfil!")
                #Sound.speak("No order!")
                time.sleep(2)
        except:
            debug_print("No connection! Try again!")
            time.sleep(2)

    return orders[current]


def delete_order(order_id):
    try:
        requests.delete(url + 'orders' + '/' +
                        order_id + '/.json', verify=False)
        debug_print("Deleted order!")
    except:
        debug_print("No connection! Try again!")
        time.sleep(1)

        delete_order(order_id)


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.pp0
    '''

    print(*args, **kwargs, file=sys.stderr)
    print(*args)
