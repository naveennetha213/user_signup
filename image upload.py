import os
import MySQLdb
from flask import Flask, request, jsonify,redirect
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
#--from werkzeug.utils import secure_filename---

upload_folder = 'folder1/folder2'
ALLOWED_EXTENSIONS = (['txt','pdf','png','jpg','jpeg','gif'])


app = Flask (__name__)
app.secret.key = '123'

app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='naveen213'
app.config['MYSQL_DB'] ='innovius'

mysql = MySQL(app)

@app.route('/img_upload', methods = ['POST'])
def img_upload():

    if request.method == 'POST':
        userid = request.json['userid']
        name = request.json['name']
        path = request.json['path']
        cursor = mysql.connection.cursor(MySQLdb.cursor.Dictcursor)
        cursor.execute(('insert into image values (%s,%s,%s)'), (userid,name, path))
        mysql.connection.commit()
        return 'success'
    else:
        return 'unsuccess'

    if __name__ == "__main__":
        app.run()

