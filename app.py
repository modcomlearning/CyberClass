from flask import *
import pymysql
app = Flask(__name__)

from functions import *
# Routes Here
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # Check if form was posted by user
    if request.method == 'POST':
            # Receive what was posted by user including username, password1,password2 email, phone
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            title = request.form['title']
	        # Now we can save username, password, email, phone into our users table
		    # Make a connection to database
            connection = pymysql.connect(host='localhost', user='root', password='',
                                             database='MbuniCyber')
		    # Create an Insert SQL, Note the SQL has 4 placeholders, Real values to be provided later			     
            sql = ''' 
                     insert into users(username, email, password, title) 
                     values(%s, %s, %s, %s)
                 '''
		    # Create a cursor to be used in Executing our SQL 
            cursor = connection.cursor()
		    # Execute SQL, providing the real values to replace our placeholders 
            cursor.execute(sql, (username, email, hash_password_salt(password), title))
		    # Commit to Save to database
            connection.commit()
		    # Return a message to user to confirm successful registration.
            return render_template('signup.html', msg='Application Made Successfully')
    else:
        # Form not posted, display the form to allow user Post something
        return render_template('signup.html')




@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='MbuniCyber')


        sql = '''
           select * from users where username = %s
        '''
        cursor = connection.cursor()
        cursor.execute(sql, (username))
        # Check if username exists

        if cursor.rowcount == 0:
             return render_template('signin.html', msg='Invalid Username')
        else:
            # Username Found, get hashed password for that username
            row = cursor.fetchone()
            hashed_password = row[2] # this is hashed password.
            # Verify if the hashed password belongs to the password user typed
            if verify_password_salt(hashed_password, password):
                 return render_template('signin.html', msg='Correct Match')
            else:
                 return render_template('signin.html', msg='Incorrect')

    else:
        return render_template('signin.html')





app.run(debug=True)