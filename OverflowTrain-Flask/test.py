import requests


URL = 'http://143.198.208.163:5000'
HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def get_orders():
    response = requests.get(f'{URL}/api/orders')
    print(response.json())


def add_order(destination):
    response = requests.post(
        f'{URL}/api/orders/add', data=f'{{"destination": "{destination}" }}', headers=HEADERS)
    print(response.json())


def pop_first_order():
    response = requests.delete(f'{URL}/api/orders/popfirst')
    print(response.json())


def clear_all_orders():
    requests.delete(f'{URL}/api/orders/clearall')


add_order("test")
add_order("test2")
add_order("test3")
pop_first_order()
get_orders()
clear_all_orders()
get_orders()
