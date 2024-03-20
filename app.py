from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the model
with open('modeldt_best.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the currency options
currency_options = [
    "US Dollar",
    "Euro",
    "Yuan",
    "UK Pound",
    "Ruble",
    "Yen",
    "Australian Dollar",
    "Rupee",
    "Shekel",
    "Canadian Dollar",
    "Swiss Franc",
    "Mexican Peso",
    "Brazil Real",
    "Bitcoin",
    "Saudi Riyal"
]

@app.route('/')
def home():
    return render_template('index.html', currency_options=currency_options)

@app.route('/predict', methods=['GET','POST'])
def predict():
    # Extract data from request form
    from_bank = int(request.form['from_bank'])
    to_bank = int(request.form['to_bank'])
    amount_received = float(request.form['amount_received'])
    receiving_currency = float(request.form['receiving_currency'])
    amount_paid = float(request.form['amount_paid'])
    payment_currency = float(request.form['payment_currency'])
    hour = int(request.form['hour'])
    minutes = int(request.form['minutes'])
    different_account = int(request.form['different_account'])
    payment_format_ach = int(request.form.get('payment_format_ach', 0))
    payment_format_bitcoin = int(request.form.get('payment_format_bitcoin', 0))
    payment_format_cash = int(request.form.get('payment_format_cash', 0))
    payment_format_cheque = int(request.form.get('payment_format_cheque', 0))
    payment_format_credit_card = int(request.form.get('payment_format_credit_card', 0))
    payment_format_reinvestment = int(request.form.get('payment_format_reinvestment', 0))
    payment_format_wire = int(request.form.get('payment_format_wire', 0))

    # Make prediction
    prediction = model.predict([[from_bank, to_bank, amount_received, receiving_currency, amount_paid,
                                  payment_currency, hour, minutes, different_account,
                                  payment_format_ach, payment_format_bitcoin, payment_format_cash,
                                  payment_format_cheque, payment_format_credit_card,
                                  payment_format_reinvestment, payment_format_wire]])[0]

    return render_template('index.html', currency_options=currency_options, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
