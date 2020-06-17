# CritBooks

#### Project 1 | CS50W | Harvardx

Web Programming with Python and JavaScript

It is a book review and rating website using Flask and Postgres. You can find more than 4999 books with exclusive reviews and ratings. Also you can find ratings from a lot of readers through [goodreads](https://goodreads.com).

### Installation

Install all dependencies by installing `requirements.txt`

Add `DATABASE_URL` to evironment variable.

Run `import.py` to setup database, create tables and import books.

## Features

### Search

`url : '/'`

Users can type the ISBN number of a book, the title of a book, or the author of a book. They can type in only part of a title, ISBN, or author name as well!

### Books

`url : '/books?search=<query>'`

After Searching a book it will redirect users to Books page where they can see a list of books matching their search query. Books will be shown in descending order according its publishing year.

### Book

`url : '/book/<ISBN>'`

Afer user click on a specific book, it will redirect to Book page, where they can see the ISBN number, the title, the author, publishing year, [goodreads](https://goodreads.com) ratings, other user's reivews and ratings. If the user is logged in then they can post their own review and rating. They can post only one review and rating.

### Login

`url : '/login'`

User can login with their credentials. After login, it will redirect to search page. But if user come from a book page and try to login, it will redirect to that previous book page.

### Sign up

`url : '/signup'`

User can Sign up setting their credentials. Username is unique, they can not use used usernames. After Sign up, it will redirect to search page. But if user come from a book page and try to Sign up, it will redirect to that previous book page.

### API Documentation

`url : '/api'`

Description of API functionalities

### API

`url : '/api/<ISBN>'`

Return json data of a book by getting a `GET` request using the ISBN number.

```
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2020,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```
