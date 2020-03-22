from flask import Flask, render_template, request, json, session, flash, redirect
import os
import pymysql.cursors
import pymysql.err


# Setting up the connection
connection = pymysql.connect(   host='localhost',
                                user='root',
                                password='pwd',
                                db='bmsproject',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)


app = Flask(__name__)


# Main Sign-In or Register page
@app.route("/")
def home():
    return render_template('loginOrSignUp.html')


# What to do when the user submits registration data
@app.route('/registrationData', methods=['POST', 'GET'])
def registrationData():
    if request.method == 'POST':
        cursor = connection.cursor()
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Read a single record
        sql = "INSERT INTO customer_info (username,email_id,password) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (name, email, password))
            connection.commit()
            return "Saved successfully. Click <a href='/'>here<a> to login"
        except pymysql.err.MySQLError as e:
            flash('Got error {!r}, errno {}'.format(e,e.args[0]))
            return redirect(request.referrer)
        cursor.close()
    else:
        return "Unknown Error. Click <a href='/'>here</a> to return back home>"



# What to do when the user tries to login
@app.route('/loginData', methods=['POST'])
def loginData():
    cursor = connection.cursor()
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']
        input_userType = str(request.form.get('userType'))

    # Database Validation and SQL Query creation for different login types
    if input_userType == "admin":
        sqlCheck = "SELECT * FROM admin_info WHERE email_id = %s"
    elif input_userType == "theaterOwner":
        sqlCheck = "SELECT * FROM theater_owner_info WHERE email_id = %s"
    else:
        sqlCheck = "SELECT * FROM customer_info WHERE email_id = %s"

    # Sending input email to database and retrieving user info
    print(sqlCheck)
    try:
        cursor.execute(sqlCheck, input_email)
        database_record = cursor.fetchone()
        connection.commit()
    except pymysql.err.MySQLError as e:
        print('Got error {!r}, errno {}'.format(e,e.args[0]))
    cursor.close()
    if database_record:
        if (database_record['password'] == input_password): # Deal with proper login credentials
            session['logged_in'] = True
            flash('Signed In')
            return "Signed in. Click <a href='/logout'>here</a> to logout"
        else: # Deal with correct email input but wrong password
            return "Unable to sign in.Click <a href='/'>here</a> to return to home"
    else:   #Deal with incorrect email but maybe correct password
        return "No record found of email and password.Click <a href='/'>here</a> to return to home"


# Route for the logout. Redirects to the main login page
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')



# Setting secret key to manage sessions and starting debugging
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
