from flask import Flask, request, render_template, flash, get_flashed_messages, redirect, url_for
import secrets
from controller import ticker_available, write_users_data




app = Flask(__name__)

@app.route('/')
def home():
   message = get_flashed_messages()
   return render_template('index.html', message = message)


@app.route('/submit-form', methods = ['POST'])
def submitForm():
    
    ticker = request.form.get('ticker')  

    if ticker_available(ticker):
        write_users_data(request.form)
        flash('Your form has been submitted successfully.', 'success')
    else:
        flash('Ticker is not available', 'danger')

    return redirect(url_for('home'))


if __name__ == '__main__':
   
   app.secret_key = secrets.token_hex(16)
   app.run(debug=True)
   