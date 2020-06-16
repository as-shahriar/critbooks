from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import csv

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine)) 


def add_books():
    """Add Books to databse"""
    global db
    with open('books.csv','r') as file:
        books = csv.reader(file)
        next(books)
        i = 0
        limit = 100
        for isbn, title,author, year in books:
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year);",{'isbn':isbn, 'title':title, 'author':author, 'year':year})
            print(i+1,title,"uploadeding...")
            i+=1
            if i==limit:
                db.commit()
                print("\nuploaded",limit,"books\n")
                limit += 100
                
                
        db.commit()
        file.close()
        print("Uploading Finished.Total uploaded",i)


def create_user_table():
    """Create User Table"""
    global db
    create_user_table = """
    CREATE TABLE users (
          id SERIAL PRIMARY KEY,
          username VARCHAR NOT NULL unique,
          password VARCHAR NOT NULL
      );
    """
    db.execute(create_user_table)
    db.commit()
    print("User Table Created")


def create_book_table():
    """Create Book Table"""
    global db
    create_book_table = """
    CREATE TABLE books (
          id SERIAL PRIMARY KEY,
          isbn VARCHAR NOT NULL,
          title VARCHAR NOT NULL,
          author VARCHAR NOT NULL,
          year VARCHAR NOT NULL
      );
    """
    db.execute(create_book_table)
    db.commit()
    print("Book Table Created")

def create_review_table():
    """Create review Table"""
    global db
    create_book_table = """
    CREATE TABLE review (
          id SERIAL PRIMARY KEY,
          username VARCHAR NOT NULL,
          review VARCHAR NOT NULL,
          rating INTEGER NOT NULL,
          book_id INT NOT NULL
      );
    """
    db.execute(create_book_table)
    db.commit()
    print("Review Table Created")


if __name__ == '__main__':
    # create_user_table()
    # create_book_table()
    create_review_table()
    # add_books()
    

