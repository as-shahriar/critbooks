
from flask import Flask, session,render_template,request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib
import os

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



def password_hash(password):
    salt = "27a0091dee99016f8fb6599da096feff"
    slat_password = password+salt
    hashed_password = hashlib.md5(slat_password.encode())
    return hashed_password.hexdigest()


@app.route("/")
def search():
    return render_template('search.html')


    

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.execute("select * from users where username=:username and password=:password;",{'username':username,'password':password_hash(password)})
        if user.rowcount == 0:
            return render_template('login.html',message="Wrong Username or Password.")
        session['logged_in'] = True
        session['username'] = request.form['username']
        return redirect(url_for("search"))

    return render_template('login.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1!=password2:
            return render_template('signup.html',message="Password did not match.")
       
        if db.execute('select username from users where username=:username;',{'username':username}).rowcount !=0:
            return render_template('signup.html',message="Username Exists. Try Another.")
        try:
            password = password_hash(password1)
            user = db.execute("insert into users (username,password) values(:username ,:password);",{'username':username,'password':password})
            db.commit()
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("search"))
        except:
            return render_template('signup.html',message="Server Error.")
    return render_template('signup.html')

@app.route("/books")
def books():
    return render_template('books.html')

@app.route("/book")
def book():
    return render_template('book.html')



@app.route("/api")
def api():
    return render_template('api.html')



@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ""
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.debug = True
    app.run()