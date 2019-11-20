
from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
from flaskext.mysql import MySQL
from flask import Flask, render_template, request
from flask import make_response
from flask import Flask, Session, redirect, url_for, escape, request

app = Flask(__name__)
my = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
my.init_app(app)
conn = my.connect()
cur =conn.cursor()
    
@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
        error = None
        if 'username' in session:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username_form  = request.form['username']
            password_form  = request.form['password']
            #s="SELECT COUNT(1) FROM sin WHERE user = '%s'" %(username_form) # CHECKS IF USERNAME EXSIST
            #cur.execute(s)
            #if cur.fetchone()[0]:
            s="SELECT password FROM sin WHERE username = '%s'" %(username_form) # FETCH THE HASHED PASSWORD
            cur.execute(s)
            for row in cur.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
        return render_template('login.html', error=error)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'admin'

if __name__ == '__main__':
    app.run(debug=True)