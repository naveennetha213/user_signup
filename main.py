import json

# import content as content
import os
# import sys

# import config
import urllib.request

from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from pip._internal.utils import datetime

upload_folder = r'D:/New folder'
import hashlib
from werkzeug.utils import secure_filename

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.secret_key = 'aaa'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['upload_folder'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MYSQL_PASSWORD'] = 'naveen213'
app.config['MYSQL_DB'] = 'innovius'

mysql = MySQL(app)


@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        name = request.form['name']
        mobilenumber = request.form['mobilenumber']
        age = request.form['age']
        address = request.form['address']
        mail_id = request.form['mail_id']
        password = request.form['password']
        image = request.form['image']
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
        password = request.json['password']
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload_folder = 'D:\a'

# @app.route('/upload', methods=['POST'])
# def upload():
# check if the post request has the file part
# if 'file' not in request.files:
#     resp = jsonify({'message': 'No file part in the request'})
#     resp.status_code = 400
#     return resp
# file = request.files['file']
# if file.filename == '':
#      resp = jsonify({'message': 'No file selected for uploading'})
#      resp.status_code = 400
#      return resp
# if file and allowed_file(file.filename):
#     filename = secure_filename(file.filename)
#     file.save(os.path.join(app.config['D:\a'], filename))
#     resp = jsonify({'message': 'File successfully uploaded'})
#     resp.status_code = 201
#     return resp
# else:
#     resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
#     resp.status_code = 400
#     return resp

@app.route('/img_upload', methods=['POST'])
def img_upload():
    global filename
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    file = request.files['file']
    path = request.form['upload_folder']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #path = upload_folder
        #resp = jsonify({'message': 'File successfully uploaded'})
        file.save(os.path.join(app.config['upload_folder'], filename))
         #path = upload_folder
        cur.execute("INSERT INTO images (file_name, uploaded_on) VALUES (%s, %s)", [filename, now])
        mysql.connection.commit()
        mysql.connection.commit()
        resp = jsonify({'message': 'File successfully uploaded'})
        return redirect(url_for('uploaded_file',
                                filename=filename))


if __name__ == "__main__":
    app.run()
