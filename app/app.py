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
        return jsonify({'id': order.id})


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
