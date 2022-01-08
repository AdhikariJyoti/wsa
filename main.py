from flask import Flask, render_template, request

# for database

from flask_mysqldb import MySQL

app = Flask(__name__)

# databse setting for mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbase_trekapp'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


# methods = is added only for post method
@app.route('/doLogin', methods=['POST'])
def doLogin():
    # 'email' is name="email" of login.html in <input of email field
    email = request.form['email']
    password = request.form['psw']

    # to give place to hit query of mysql->cursor
    cursor = mysql.connection.cursor()
    resp = cursor.execute(
        '''SELECT * FROM users WHERE email=%s and password=%s;''', (email, password))

    # fetchall() is for select
    user = cursor.fetchall()
    print(user)
    # if  email/password entered and email/password in database match response=1
    if resp == 1:
        return render_template('home.html', result=user)
    else:
        return render_template('login.html', result="Invalid Credentials")


@app.route('/doRegister', methods=['POST'])
def doRegister():
    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    address = request.form['address']

    password = request.form['psw']
    print(full_name)

    cursor = mysql.connection.cursor()
    resp = cursor.execute('''INSERT INTO `users` (`id`, `full_name`, `address`, `email`, `phone_number`, `password`) VALUES (NULL, %s, %s, %s, %s, %s);''',
                          (full_name, address, email, phone_number, password))

    # .commit() is needed to be done for all the sql quries where you add some data to table like insert and update but not select
    mysql.connection.commit()
    # mysql.connection.close()

    print(resp)

    # return "Hello"

    if resp == 1:
        return render_template('login.html')
    else:
        return render_template('register.html', result="User not registered successfully")


@app.route('/treks')
def allTreks():

    email = request.form['email']
    password = request.form['psw']

    cursor = mysql.connection.cursor()
    treks = cursor.execute(
        '''SELECT * FROM users WHERE email=%s and password=%s;''', (email, password))
    return render_template('listing.html', result=treks)


app.run()
