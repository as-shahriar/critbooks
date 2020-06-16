
from flask import Flask, session,render_template,request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib
import os
import requests

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
    isbn = request.args.get('next')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.execute("select * from users where username=:username and password=:password;",{'username':username,'password':password_hash(password)})
        if user.rowcount == 0:
            return render_template('login.html',message="Wrong Username or Password.")
        session['logged_in'] = True
        session['username'] = request.form['username']
        if isbn:
            return redirect(url_for("book",isbn=isbn))
        return redirect(url_for("search"))

    return render_template('login.html',next=isbn)

@app.route("/signup",methods=['GET','POST'])
def signup():
    isbn = request.args.get('next')
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
            if isbn:
                return redirect(url_for("book",isbn=isbn))
            return redirect(url_for("search"))
        except:
            return render_template('signup.html',message="Server Error.")
    return render_template('signup.html',next=isbn)



@app.route("/books")
def books():
    q = request.args.get('search')
    if q != None:
        q = q.strip().replace("'","")
        obj_books = db.execute("select * from books where isbn LIKE ('%"+q+"%')  or lower(title) LIKE lower('%"+q+"%') or  lower(author) LIKE lower('%"+q+"%') or (year = '"+q+"') order by year desc;").fetchall() 
        count = len(obj_books)
        if count == 0:
            return render_template('books.html',q=q,count=count,message="404 Not Found")


        
        return render_template('books.html',q=q,count=count,obj_books=obj_books)
    return render_template('books.html')


@app.route("/book/<isbn>",methods=['GET','POST'])
def book(isbn):
    message = None
    is_reviewed = False
    if request.method == "POST" and session['logged_in']:
        my_rating = request.form.get('rating')
        my_review = request.form.get('review')
        book_id = request.form.get('book_id')
        if my_review.strip()=="" or my_rating=="":
            message = "Invalid Review"
        else:
            db.execute("insert into review (username, review, rating, book_id) select :username,:review,:rating,:book_id where not exists (select * from review where username = :username and book_id = :book_id);",
            {
                'username': session['username'],
                'review': my_review,
                'rating':my_rating,
                'book_id': book_id    
            })
            db.commit()
            is_reviewed = True



    res = db.execute("select * from books where isbn=:isbn;",{'isbn':isbn}).fetchone() 
    if res==None:
        return render_template('book.html')
    


    reviews = db.execute("select * from review where book_id=:id;",{'id':res.id}).fetchall()
    if request.method == "GET":
        try:
            if session['logged_in']:
                check_review = db.execute("select username from review where book_id=:id and username=:username;",
            {
                'id':res.id,
                'username': session['username']  
            }).fetchone()
                if check_review != None:
                    is_reviewed = True
        except:
            pass
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("KEY"), "isbns": isbn})
        value = response.json().get('books')[0]
        count = value.get('work_ratings_count')
        rating = value.get('average_rating')
    except:
        count = "loading"
        rating = "loading"
    return render_template('book.html',obj_book=res,count=count,rating=rating,reviews=reviews,message=message,is_reviewed=is_reviewed)



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