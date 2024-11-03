import random
import re
import mailtrap as mt
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'  # Replace with a strong secret key

# Function to get a MySQL connection
def get_mysql_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='flutter',
        cursorclass=pymysql.cursors.DictCursor,
        ssl_disabled=True  # Explicitly disable SSL
    )

@app.route('/register', methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        connection = get_mysql_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
                
                # Send OTP via Mailtrap
                mail = mt.Mail(
                    sender=mt.Address(email="hello@demomailtrap.com", name="Mailtrap Test"),
                    to=[mt.Address(email=email)],
                    subject="Your OTP Code",
                    text=f"Your OTP code is: {otp}"
                )

                client = mt.MailtrapClient(token="f1452a73ff543fa355c00479d6eaa57b")
                response = client.send(mail)

                # Store OTP in database with expiration time
                expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)  # Set OTP expiration to 5 minutes
                cursor.execute(
                    'INSERT INTO otp_verification (username, password, email, otp, expires_at) VALUES (%s, %s, %s, %s, %s)', 
                    (username, password, email, otp, expires_at)
                )
                connection.commit()

                return jsonify({'message': 'OTP sent to email!', 'status': 'success'})
        
        except Exception as e:
            msg = f'An error occurred: {str(e)}'
        finally:
            connection.close()
        
    return jsonify({'message': msg, 'status': 'fail'})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    msg = ''
    if request.method == 'POST' and 'otp' in request.form:
        otp = request.form['otp']
        
        # Verify OTP from database
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM otp_verification WHERE otp = %s', (otp,))
        record = cursor.fetchone()

        if record:
            # Check if OTP has expired
            if record['expires_at'] > datetime.datetime.now():
                # Save user in the database (consider hashing the password)
                cursor.execute(
                    'INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', 
                    (record['username'], record['password'], record['email'])  # Store actual data
                )
                connection.commit()
                # Optionally delete the record after verification
                cursor.execute('DELETE FROM otp_verification WHERE otp = %s', (otp,))
                connection.commit()
                msg = 'Registration successful!'
            else:
                msg = 'OTP has expired!'
        else:
            msg = 'Invalid OTP!'

    return jsonify({'message': msg, 'status': 'fail'})

@app.route('/login', methods=['POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        connection = get_mysql_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            if account:
                # Generate JWT token
                token = jwt.encode({
                    'user_id': account['id'],  # Include user ID in token payload
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
                }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
                
                return jsonify({'message': 'Logged in successfully!', 'token': token})
            else:
                msg = 'Incorrect username/password!'
        except Exception as e:
            msg = f'An error occurred: {str(e)}'
        finally:
            connection.close()

    return jsonify({'message': msg, 'status': 'fail'})

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')  # Get token from the request header
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    
    try:
        data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Protected route accessed!', 'user_id': data['user_id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
