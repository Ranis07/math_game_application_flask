#==========importing libraries & modules===========
from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import timedelta
import pymysql
import smtplib
#===inheriting local module
import pwd
import api 


#========Configuration of Flask App=========
app = Flask(__name__)
app.config['SECRET_KEY'] = pwd.secret
#=======configuring session time
app.permanent_session_lifetime = timedelta(minutes=20)


#=========Database Connection=============
class Database:
    """MySQL Database"""
    def connection(self):
        """Establishes connection with the database
        :return: Connection of the application with database
        """
        connect = pymysql.connect(host='localhost', user=pwd.db_root, password=pwd.db_password, database=pwd.database)
        return connect

#======instanciating class 'Database'
db = Database() 
con = db.connection()


#=============routes===============

#==========routes for register page
@app.route("/", methods=['GET','POST'])
@app.route("/register", methods=['GET','POST'])
def register():
    """"If true, register user into the database through POST method form, then redirects to login page, else false
    :return: register.html template and API data
    """
    #====Assigning variables for API
    text_api = api.confirmed
    text_api1 = api.lastupdate

    if request.method == 'POST': #if the 'submit' button hit in 'register.html', it executes
        userDetails = request.form #this is form that is in its frontend part
        fullname = userDetails['full-name'] #accessing 'fullname' from the form and likewise
        email = userDetails['email']
        password = userDetails['password']
        cpassword = userDetails['c-password']

        #========executing SQL query
        cur = con.cursor()
        cur.execute('select email from users where email=%s', email)
        row = cur.fetchone()

        if row != None:
            flash("Oops!! Could Not Signup, That Email Already Exist. Try Again!!",'danger')
            return redirect(url_for('register'))
        elif password != cpassword:
            flash("Oops!! Passwords Did Not Match With Each Other. Try Again!!",'danger')
            return redirect(url_for('register'))
        elif not fullname or not email or not password or not cpassword:
            flash("Oops!! All Field Should Be Filled!!",'danger')
            return redirect(url_for('register'))
        else:
            cur.execute('insert into users(full_name, email, password) values(%s,%s,%s)',(fullname,email,password))
            con.commit()
            flash(f"Account created successfully. Now you may login.",'success')
            return redirect(url_for('login'))
            
    return render_template('register.html', text_api=text_api, text_api1=text_api1, title='Register')


#==========routes for login page
@app.route('/login', methods=['GET','POST'])
def login():
    """"If true, logs in user through POST method form, creates session,
    then redirects to main game page, else false
    :return: login.html template and API data
    """
    text_api = api.confirmed
    text_api1 = api.lastupdate
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']

        cur = con.cursor()
        cur.execute('select * from users where email=%s and password=%s',(email, password)) 
        row = cur.fetchone()

        if row == None:
            flash("Oops!! Either Entered Data Is Incorrect Or!! That Account Doesn't Exist!! Try Again.",'danger')
            return redirect(url_for('login'))
        else:
            #=========using flask session
            session.permanent = True #by default it's 'False'
            session['email'] = email
            return redirect(url_for('index'))

    return render_template('login.html', text_api=text_api, text_api1=text_api1, title='Login')


#==========routes for index/mathgame page
@app.route('/index')
def index():
    """"If in session, redirects user to play game, else false
    :return: index.html template and name of the player from database
    """
    #=====searching 'email' key in session dictionary
    if 'email' in session:
        cur = con.cursor()
        cur.execute('select full_name from users where email=%s', session['email'])
        row = cur.fetchone()
        return render_template('index.html', name=row)
    else:
        flash('Oh! Oh! You Have To Login First.','danger')
        return redirect(url_for('login'))


#==========routes for forgot password page
@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    """"If true, sends password reset link to the user via email, else false
    :return: forgotpassword.html template and API data
    """
    text_api = api.confirmed
    text_api1 = api.lastupdate
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']

        cur = con.cursor()
        cur.execute('select email from users where email=%s', email)
        row = cur.fetchone()

        if row != None:
            #===these code links the application with email
            subject = 'Password Reset Confirmation'
            body = ' Reset password through this: http://127.0.0.1:5000/reset_password'
            message = f"Subject: {subject}\n\n{body}"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(pwd.email, pwd.pwd)
            server.sendmail(pwd.email, email, message) #sending mail

            flash("Email For 'Password Reset' Has Been Sent.",'success')
            return redirect(url_for('login'))
        elif not email:
            flash("Oops!! Email Field Is Required!!",'danger')
            return redirect(url_for('forgot_password'))
        else:
            flash("Oops!! This Account Doesn't Exist. Try Signing Up First.",'danger')
            return redirect(url_for('register'))

    return render_template('forgotpassword.html', title='Forgot Password', text_api=text_api, text_api1=text_api1)


#==========routes for reset password page
@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    """"If true, make changes or resets the password in the database,
    and redirects to login page, else false
    :return: resetpassword.html template and API data
    """
    text_api = api.confirmed
    text_api1 = api.lastupdate
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        cpassword = userDetails['c-password']

        cur = con.cursor()
        cur.execute('select email from users where email=%s', email)
        row = cur.fetchone()

        if row != None:
            cur.execute('update users set password=%s where email=%s', (password,email)) #using update SQL query
            con.commit()
            flash('Your Password Has Been Reset. Now You May Login.','success')
            return redirect(url_for('login'))
        elif not password or not cpassword:
            flash("Oops!! All Fields Are Required!!",'danger')
            return redirect(url_for('reset_password'))
        elif password != cpassword:
            flash("Oops!! Passwords Did Not Match With Each Other. Try Again!!",'danger')
            return redirect(url_for('reset_password')) 
        else:
            flash("Oops!! This Account Doesn't Exist. Try Signing Up First.",'danger')
            return redirect(url_for('register'))

    return render_template('resetpassword.html', title='Reset Password', text_api=text_api, text_api1=text_api1)


#==========routes for logout page
@app.route('/logout')
def logout():
    """"Logs out user from the system, destroys session and redirects to login page
    :return: login.html template
    """
    #=======destroying session
    session.pop('email', None)
    flash('You Have Been Successfully Logged Out.','success')
    return redirect(url_for('login'))


#=======is used to execute code only if the file was run directly, and not imported=======
if __name__ == '__main__':
    app.run(debug=True) # debug=True is you don't have to start server again&again after making changes