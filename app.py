from flask import Flask, render_template, request, redirect, url_for
from repl import DatabaseEngine

app = Flask(__name__)
db = DatabaseEngine()

@app.route('/')
def index():
    merchants = db.execute("SELECT * FROM Merchants")
    transactions = db.execute("SELECT * FROM Transactions")
    return render_template('index.html', merchants=merchants, transactions=transactions)

@app.route('/add_merchant', methods=['GET', 'POST'])
def add_merchant():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        result = db.execute(f'INSERT INTO Merchants VALUES ("{name}", "{email}")')
        print(result)
        db.save()
        return redirect(url_for('index'))
    return render_template('add.html', type='Merchant')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        merchant_id = request.form['merchant_id']
        amount = request.form['amount']
        payment_method = request.form['payment_method']
        result = db.execute(f'INSERT INTO Transactions VALUES ({merchant_id}, {amount}, "{payment_method}")')
        print(result)
        db.save()
        return redirect(url_for('index'))
    return render_template('add.html', type='Transaction')

@app.route('/edit_merchant/<int:merchant_id>', methods=['GET', 'POST'])
def edit_merchant(merchant_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        db.execute(
            f'UPDATE Merchants SET name="{name}" WHERE merchant_id={merchant_id}'
        )
        db.execute(
            f'UPDATE Merchants SET email="{email}" WHERE merchant_id={merchant_id}'
        )

        return redirect(url_for('index'))

    merchant = db.execute(
        f'SELECT * FROM Merchants WHERE merchant_id={merchant_id}'
    )[0]

    return render_template('edit.html', type='Merchant', row=merchant)

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        merchant_id = request.form['merchant_id']
        amount = request.form['amount']
        payment_method = request.form['payment_method']

        db.execute(
            f'UPDATE Transactions SET merchant_id={merchant_id} WHERE transaction_id={transaction_id}'
        )
        db.execute(
            f'UPDATE Transactions SET amount={amount} WHERE transaction_id={transaction_id}'
        )
        db.execute(
            f'UPDATE Transactions SET payment_method="{payment_method}" WHERE transaction_id={transaction_id}'
        )

        return redirect(url_for('index'))

    transaction = db.execute(
        f'SELECT * FROM Transactions WHERE transaction_id={transaction_id}'
    )[0]

    return render_template('edit.html', type='Transaction', row=transaction)


if __name__ == "__main__":
    app.run(debug=True)
