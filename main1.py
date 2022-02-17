import hashlib
import os
import urllib.request

import MySQLdb
from flask import Flask, request, redirect, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'aaa'
UPLOAD_FOLDER = r'D:/New folder'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MYSQL_PASSWORD'] = 'naveen213'
app.config['MYSQL_DB'] = 'innovius'

mysql = MySQL(app)


@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emp_id = request.json['emp_id']
        name = request.json['name']
        mobilenumber = request.json['mobilenumber']
        age = request.json['age']
        address = request.json['address']
        mail_id = request.json['mail_id']
        password = request.json['password']
        image = request.json['image']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into emp_registration values(%s,%s,%s,%s,%s,%s,%s,%s)', (
            emp_id, name, mobilenumber, age, address, mail_id, password, image))
        mysql.connection.commit()
        return 'Registration successful'
    else:
        return " registration was un successful"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail_id = request.json['mail_id']
        request.json['password']
        hashedpassword = hashlib.sha256(request.form['password'].encode())
        password = hashedpassword.hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from emp_registration where mail_id=%s and password=%s", (mail_id, password))
        emp_registration = cursor.fetchone()
        print(emp_registration)
        if emp_registration:
            emp_registration['mail_id'] = mail_id
            emp_registration['password'] = password

        return 'login successful'
    return "invalid credential"


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file_upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    app.run()
