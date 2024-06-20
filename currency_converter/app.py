from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '4b58b29e84736e407957914c'
BASE_URL = 'https://v6.exchangerate-api.com/v6'


def get_exchange_rate(from_currency, to_currency):
    url = f"{BASE_URL}/{API_KEY}/latest/{from_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates'].get(to_currency)
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    converted_amount = None
    error_message = None

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency']
            to_currency = request.form['to_currency']

            rate = get_exchange_rate(from_currency, to_currency)

            if rate is None:
                error_message = 'Error fetching conversion rate.'
            else:
                converted_amount = amount * rate

        except ValueError:
            error_message = 'Error fetching conversion rate.'

    return render_template('index.html', converted_amount=converted_amount, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
