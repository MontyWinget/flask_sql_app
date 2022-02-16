from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

# Object init to run flask app
app = Flask(__name__)

# Configure DB
db = yaml.full_load((open('db.yaml')))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        user_details = request.form
        name = user_details['Name']
        email = user_details['Email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) Values(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')


@app.route('/users')
def users():
    cursor = mysql.connection.cursor()
    cur = cursor
    result_value = cur.execute("SELECT * FROM users")
    if result_value > 0:
        user_details = cur.fetchall()
        return render_template('users.html', user_details=user_details)


if __name__ == '__main__':
    app.run(debug=True)

