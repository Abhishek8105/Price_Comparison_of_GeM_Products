from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'Your_secret_key_here'
app.template_folder = '../templates'
app.static_folder = '../static'

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = users[email]
            return redirect(url_for('profile'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['pass']
        cpass = request.form['cpass']
        if password == cpass:
            users[email] = {'first_name': f_name, 'last_name': l_name, 'phone': phone, 'password': password}
            return redirect(url_for('login'))
        return 'Passwords do not match'
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'user' in session:
        user = session['user']
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new-password']
        if email in users:
            users[email]['password'] = new_password
            return redirect(url_for('login'))
        return 'Email not found'
    return render_template('forgotpassword.html')

@app.route('/ontactus')
def contactus():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
