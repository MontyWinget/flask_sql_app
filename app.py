from flask import Flask, render_template, request, redirect, jsonify, json
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import yaml

# Object init to run flask app
app = Flask(__name__)
CORS(app)

# Configure DB
db = yaml.full_load((open('db.yaml')))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['POST'])
@cross_origin()
def index():
    data = request.get_json()
    name = data['name']
    email = data['email']
    print(name)
    print(email)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name, email) Values(%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    # return redirect('/users')
    return "Success"


@app.route('/users')
@cross_origin()
def users():
    cursor = mysql.connection.cursor()
    cur = cursor
    result_value = cur.execute("SELECT * FROM users")
    if result_value > 0:
        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        return jsonify(json_data)
    return jsonify(welcome='cross-origin working')


if __name__ == '__main__':
    app.run(debug=True)
#
#     if result_value > 0:
#         # user_details = cur.fetchall()
#         row_headers = [x[0] for x in cur.description]  # this will extract row headers
#         rv = cur.fetchall()
#         json_data = []
#         for result in rv:
#             json_data.append(dict(zip(row_headers, result)))
#         return jsonify(json_data)
#         # for user in user_details:
#         #     user_details_dict['Name'] = user[0]
#         #     user_details_dict['Email'] = user[1]
#         # # return render_template('html.file', user_details=user_details)
#         # return user_details_dict
#     return jsonify(welcome='cross-origin working')
