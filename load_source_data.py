from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    with open('purchases.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

