import json
import flask
from flask import request, render_template, abort, jsonify


ordersQueue = []


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/orders', methods=['GET'])
def orders():
    return jsonify(ordersQueue)


@app.route('/api/orders/add', methods=['POST'])
def orders_add():
    data = request.data.decode("utf-8")
    destination_entry = json.loads(data)
    ordersQueue.append(destination_entry)
    return jsonify(ordersQueue)


@app.route('/api/orders/popfirst', methods=['DELETE'])
def orders_poplast():
    if len(ordersQueue) <= 0:
        abort(404, description="No orders left.")

    deleted = ordersQueue.pop(0)
    return jsonify(deleted)


@app.route('/api/orders/clearall', methods=['DELETE'])
def orders_clearall():
    ordersQueue.clear()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5550)
