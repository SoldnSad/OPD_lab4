from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Замените на ваш API ключ
API_KEY = '4b58b29e84736e407957914c'
BASE_URL = 'https://v6.exchangerate-api.com/v6'

def get_exchange_rate(from_currency, to_currency):
    url = f"{BASE_URL}/{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates'][to_currency]

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_amount = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        rate = get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
    return render_template('index.html', converted_amount=converted_amount)

if __name__ == '__main__':
    app.run(debug=True)
