from flask import Flask, render_template, render_template,flash,request,redirect,url_for,jsonify,send_from_directory,send_file,Response, secure_filename
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "(*&$^JSDHDjdffjjfp;pwwdm&)%$(&)$"

import re,platform
import sqlite3
conn = sqlite3.connect("database.db",check_same_thread=False,timeout=30000)
c=conn.cursor()

opsystem=platform.system()
if opsystem=='Windows':
	app.config['UPLOAD_FOLDER'] = '.\\uploads'
	debug=True
else:
	app.config['UPLOAD_FOLDER'] = './uploads'



@app.route('/uploads/<username>',  methods=["POST", "GET"])
def uploads(username):
    file=request.files['file']
	# filename=""
    # username = request.form['username']
	if file.filename != '':
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#check file name
		# filename	
        c.execute('select uploads from user where username = ?', (username,))
        list_fn = c.fetchone()
		if(list_fn != None):
            list_fn = list_fn.split('#')
        else :
            list_fn = []
        list_fn.append(filename)
        listfn = '#'.join(list_fn)
        
        c.execute('update table user set uploads = ? where username = ?', (listfn, username,))
        print('uploaded')
		
        
        conn.commit()

		flash("Assignment Submitted")
	# return url_for('send',data="",file=file_name)
	return redirect(url_for("viewAss",cls_id=ass_id.split("_")[-2]))

@app.route('/',  methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    username = request.form['username']
    password = request.form['password']
    c.execute('select * from user where username = ?', (username,))
    result = c.fetchone()

    if not result:
        flash('user not found')
        return redirect('/')
    if password != result[2]:
        flash('Invalid password')
        return redirect('/')
    return redirect(f'/uploads/{username}')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    c.execute('INSERT INTO user(name, username, password, uploads) VALUES(?,?,?,?)', (name, username, password, ''))
    conn.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)