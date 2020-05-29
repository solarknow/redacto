import io

from flask import Flask, request, jsonify
from pdfminer import high_level

from helpers.parser import Order

app = Flask(__name__)


@app.route('/request', methods=['POST'])
def deidentify():
    if request.content_type.startswith('application/pdf'):
        raw = io.BytesIO(request.get_data())
        parsed_lines = high_level.extract_text(raw)
        order = Order(parsed_lines.splitlines(keepends=False))
        return jsonify({'id': order.id,
                        'date_placed': order.date_placed,
                        'order_total': order.order_total,
                        'items': [{"name": item.name,
                                   "quantity": item.quantity,
                                   "price": item.price,
                                   "sold_by": item.sold_by,
                                   "condition": item.condition} for item in order.items],
                        'date_shipped': order.date_shipped,
                        'shipping_loc': order.shipping_loc,
                        'shipping_speed': order.shipping_speed,
                        'payment_method': order.payment_method,
                        'billing_loc': order.billing_loc
                        })


if __name__ == '__main__':
    app.run(host='localhost')
