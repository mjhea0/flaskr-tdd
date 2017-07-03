# Flaskr - Intro to Flask, Test Driven Development, and jQuery

[![Build Status](https://travis-ci.org/mjhea0/flaskr-tdd.svg?branch=master)](https://travis-ci.org/mjhea0/flaskr-tdd)

As many of you know, Flaskr - a mini-blog-like-app - is the app you build for the official [tutorial](http://flask.pocoo.org/docs/tutorial/introduction/) for Flask, the awesome, Python-based micro web framework. I've gone through the tutorial more times than I care to admit. Anyway, I wanted to take the tutorial a step further by adding test driven development and a bit of jQuery. This post is that tutorial. Enjoy.

Also, if you are completely new to Flask and/or web development in general, it's important to grasp these basic fundamental concepts:

1. The difference between GET and POST requests and how functions within the app handle each.
1. What a "request" is.
1. How HTML pages are rendered and/or returned to the end user.

> **NOTE**: This tutorial is powered by **[Real Python](https://realpython.com)**. Please support this open source project by purchasing our [courses](http://www.realpython.com/courses) to learn Python and web development with Django and Flask!

### Change Log

- 07/03/2017: Updated to Python 3.6.1
- 01/24/2016: Updated to Python 3! (v3.5.1)
- 08/24/2014: PEP8 updates.
- 02/25/2014: Upgraded to SQLAlchemy.
- 02/20/2014: Completed AJAX.
- 12/06/2013: Added Bootstrap 3 styles
- 11/29/2013: Updated unit tests.
- 11/19/2013: Fixed typo. Updated unit tests.
- 11/11/2013: Added information on requests.

### Contents

1. [Test Driven Development?](#test-driven-development)
1. [Download Python](#download-python)
1. [Project Setup](#project-setup)
1. [First Test](#first-test)
1. [Flaskr Setup](#flaskr-setup)
1. [Second Test](#second-test)
1. [Database Setup](#database-setup)
1. [Templates and Views](#templates-and-views)
1. [Add Some Color](#add-some-color)
1. [Test](#test)
1. [jQuery](#jquery)
1. [Deployment](#deployment)
1. [Test (again!)](#test-again)
1. [Bootstrap](#bootstrap)
1. [SQLAlchemy](#sqlalchemy)
1. [Conclusion](#conclusion)

### Requirements

This tutorial utilizes the following requirements:

1. Python v3.6.1
1. Flask v0.12.2
1. Flask-SQLAlchemy v2.1
1. gunicorn v19.7.1

## Test Driven Development?

![tdd](https://raw.githubusercontent.com/mjhea0/flaskr-tdd/master/tdd.png)

Test Driven Development (TDD) is an iterative development cycle that emphasizes writing automated tests before writing the actual feature of function. Put another way, TDD combines building and testing. This process not only helps ensure correctness of the code - but also helps to indirectly evolve the design and architecture of the project at hand.

TDD usually follows the "Red-Green-Refactor" cycle, as shown in the image above:

1. Write a test
2. Run the test (it should fail)
3. Write just enough code for the test to pass
4. Refactor code and retest, again and again (if necessary)

## Download Python

Before beginning make sure you have the latest version of [Python 3.6](https://www.python.org/downloads/release/python-360/) installed, which you can download from http://www.python.org/download/.

> **NOTE**: This tutorial uses Python v3.6.1.

Along with Python, this also installed-
- [pip](https://pip.pypa.io/en/stable/) - a [package management](http://en.wikipedia.org/wiki/Package_management_system) system for Python, similar to gem or npm for Ruby and Node, respectively.
- [pyvenv](https://docs.python.org/3/library/venv.html) - used to create isolated environments for development. This is standard practice. Always, always, ALWAYS utilize virtual environments. If you don't, you will eventually run into problems with compatibility between different dependencies. Just do it.

## Project Setup

1. Create a new directory to store the project:

  ```sh
  $ mkdir flaskr-tdd
  $ cd flaskr-tdd
  ```

1. Create and activate your virtual env:

  ```sh
  $ python3 -m venv env
  $ source env/bin/activate
  ```

  > **NOTE**: You know that you are in a virtual env, as the actual "env" is now show before the $ in your terminal - (env). To exit the virtual environment, use the command `deactivate`, then you can reactivate by navigating back to the directory and running - `source env/bin/activate`.

1. Install Flask with pip:

  ```sh
  (env)$ pip install flask==0.12.2
  ```

## First Test

Let's start with a simple "hello, world" app.

1. Create a test file:

  ```sh
  (env)$ touch app-test.py
  ```

  Open this file in your favorite text editor. (I use [Sublime](http://www.sublimetext.com/).) Add the following code:

  ```python
  from app import app

  import unittest


  class BasicTestCase(unittest.TestCase):

      def test_index(self):
          tester = app.test_client(self)
          response = tester.get('/', content_type='html/text')
          self.assertEqual(response.status_code, 200)
          self.assertEqual(response.data, b'Hello, World!')


  if __name__ == '__main__':
      unittest.main()
  ```

  Essentially, we're testing whether the response that we get back is "200" and that "Hello, World!" is displayed.

1. Run the test

  ```sh
  (env)$ python app-test.py
  ```

  If all goes well, this will fail.

1. Now add the code for this to pass.

  ```sh
  (env)$ touch app.py
  ```

  Code:

  ```python
  from flask import Flask

  app = Flask(__name__)


  @app.route("/")
  def hello():
      return "Hello, World!"


  if __name__ == "__main__":
      app.run()
  ```

1. Run the app:

  ```sh
  (env)$ python app.py
  ```

  Then Navigate to [http://localhost:5000/](http://localhost:5000/). You should see "Hello, World!" on your screen.

  Return to the terminal. Kill the server with Ctrl+C.

1. Run the test again:

  ```sh
  (env)$ python app-test.py
  .
  ----------------------------------------------------------------------
  Ran 1 test in 0.016s

  OK
  ```

  Nice.

## Flaskr Setup

1. Add structure

  Add two folders, "static" and "templates", in the project root. Your file structure should now look like this:

  ```sh
  ├── app-test.py
  ├── app.py
  ├── static
  └── templates
  ```

1. SQL Schema

  Create a new file called "schema.sql" and add the following code:

  ```python
  drop table if exists entries;
  create table entries (
    id integer primary key autoincrement,
    title text not null,
    text text not null
  );
  ```

  This will setup a single table with three fields - "id", "title", and "text". SQLite will be used for our RDMS since it's built in to the standard Python library and requires no configuration.

## Second Test

Let's create the basic file for running our application. Before that though, we need to write a test first.

1. Simply alter *app-test.py*:

  ```python
  from app import app

  import unittest


  class BasicTestCase(unittest.TestCase):

      def test_index(self):
          tester = app.test_client(self)
          response = tester.get('/', content_type='html/text')
          self.assertEqual(response.status_code, 404)

  if __name__ == '__main__':
      unittest.main()
  ```

  So, we are expecting a 404 error. Run the test. This will fail. Why does this fail? Simple. We are expecting a 404, but we actually get a 200 back since the route exists.

1. Update *app.py*:

  ```python
  # imports
  import sqlite3
  from flask import Flask, request, session, g, redirect, url_for, \
       abort, render_template, flash, jsonify

  # configuration
  DATABASE = 'flaskr.db'
  DEBUG = True
  SECRET_KEY = 'my_precious'
  USERNAME = 'admin'
  PASSWORD = 'admin'

  # create and initialize app
  app = Flask(__name__)
  app.config.from_object(__name__)


  if __name__ == '__main__':
      app.run()
  ```

  Here, we add in all required imports, create a configuration section for global variables, initialize the app, and then finally run the app.

1. Run it:

  ```sh
  (env)$ python app.py
  ```

  Launch the server. You should see the 404 error because no routes or views are setup. Return to the terminal. Kill the server. Now run the unit test. It should pass.

## Database Setup

Essentially, we want to open a database connection, create the database based on the schema if it doesn't already exist, then close the connection each time a test is ran.

1. How do we test for the existence of a file? Update *app-test.py*:

  ```python
  import unittest
  import os
  from app import app


  class BasicTestCase(unittest.TestCase):

      def test_index(self):
          tester = app.test_client(self)
          response = tester.get('/', content_type='html/text')
          self.assertEqual(response.status_code, 404)

      def test_database(self):
          tester = os.path.exists("flaskr.db")
          self.assertTrue(tester)


  if __name__ == '__main__':
      unittest.main()
  ```

  Run it to make sure it fails, indicating that the database does not exist.

1. Now add the following code to *app.py*:

  ```python
  # connect to database
  def connect_db():
      """Connects to the database."""
      rv = sqlite3.connect(app.config['DATABASE'])
      rv.row_factory = sqlite3.Row
      return rv


  # create the database
  def init_db():
      with app.app_context():
          db = get_db()
          with app.open_resource('schema.sql', mode='r') as f:
              db.cursor().executescript(f.read())
          db.commit()


  # open database connection
  def get_db():
      if not hasattr(g, 'sqlite_db'):
          g.sqlite_db = connect_db()
      return g.sqlite_db


  # close database connection
  @app.teardown_appcontext
  def close_db(error):
      if hasattr(g, 'sqlite_db'):
          g.sqlite_db.close()
  ```

  And add the `init_db()` function at the bottom of `app.py` to make sure we start the server each time with a fresh database:

  ```python
  if __name__ == '__main__':
      init_db()
      app.run()
  ```

  Now it is possible to create a database by starting up a Python shell and importing and calling the `init_db()` function:

  ```python
  >>> from app import init_db
  >>> init_db()
  ```

  Close the shell, then run the test again. Does it pass? Now we know that the database has been created.

## Templates and Views

Next, we need to set up the Templates and associated Views, which define the routes. Think about this from a user standpoint. We need to log users in and out. Once logged in, users need to be able to post. Finally, we need to display posts.

Write some tests for this first.

### Unit Tests

Take a look at the final code. I added docstrings for explanation.

```python
import unittest
import os
import tempfile
import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        """initial test. ensure that the database exists"""
        tester = os.path.exists("flaskr.db")
        self.assertEqual(tester, True)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    # assert functions

    def test_empty_db(self):
        """Ensure database is blank"""
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(
            app.app.config['USERNAME'] + 'x',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in rv.data
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid password' in rv.data

    def test_messages(self):
        """Ensure that user can post messages"""
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
```

If you run the tests now, all will fail except for `test_database()`:

```sh
python app-test.py
.FFFF
======================================================================
FAIL: test_index (__main__.BasicTestCase)
initial test. ensure flask was set up correctly
----------------------------------------------------------------------
Traceback (most recent call last):
  File "app-test.py", line 13, in test_index
    self.assertEqual(response.status_code, 200)
AssertionError: 404 != 200

======================================================================
FAIL: test_empty_db (__main__.FlaskrTestCase)
Ensure database is blank
----------------------------------------------------------------------
Traceback (most recent call last):
  File "app-test.py", line 51, in test_empty_db
    assert b'No entries here so far' in rv.data
AssertionError

======================================================================
FAIL: test_login_logout (__main__.FlaskrTestCase)
Test login and logout using helper functions
----------------------------------------------------------------------
Traceback (most recent call last):
  File "app-test.py", line 59, in test_login_logout
    assert b'You were logged in' in rv.data
AssertionError

======================================================================
FAIL: test_messages (__main__.FlaskrTestCase)
Ensure that user can post messages
----------------------------------------------------------------------
Traceback (most recent call last):
  File "app-test.py", line 84, in test_messages
    assert b'&lt;Hello&gt;' in rv.data
AssertionError

----------------------------------------------------------------------
Ran 5 tests in 0.088s

FAILED (failures=4)
```

Let's get these all green, one at a time...

### Show Entries

1. First, add a View for displaying the entries to *app.py*:

  ```python
  @app.route('/')
  def show_entries():
      """Searches the database for entries, then displays them."""
      db = get_db()
      cur = db.execute('select * from entries order by id desc')
      entries = cur.fetchall()
      return render_template('index.html', entries=entries)
  ```

1. Then add the *index.html* template to the "templates" folder:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <title>Flaskr</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>

    <div class="page">

      <h1>Flaskr-TDD</h1>
      <div class="metanav">
        {% if not session.logged_in %}
          <a href="{{ url_for('login') }}">log in</a>
        {% else %}
          <a href="{{ url_for('logout') }}">log out</a>
        {% endif %}
      </div>
      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}
      {% block body %}{% endblock %}

      {% if session.logged_in %}
        <form action="{{ url_for('add_entry') }}" method="post" class="add-entry">
          <dl>
            <dt>Title:</dt>
            <dd><input type="text" size="30" name="title"></dd>
            <dt>Text:</dt>
            <dd><textarea name="text" rows="5" cols="40"></textarea></dd>
            <dd><input type="submit" value="Share"></dd>
          </dl>
        </form>
      {% endif %}
      <ul class="entries">
        {% for entry in entries %}
          <li><h2>{{ entry.title }}</h2>{{ entry.text|safe }}</li>
        {% else %}
          <li><em>No entries yet. Add some!</em></li>
        {% endfor %}
      </ul>

    </div>

  </body>
  </html>
  ```

1. Run the tests now. You should see:

  ```sh
  Ran 5 tests in 0.131s

  FAILED (failures=2, errors=2)
  ```

### User Login and Logout

1. Update *app.py*:

  ```python
  @app.route('/login', methods=['GET', 'POST'])
  def login():
      """User login/authentication/session management."""
      error = None
      if request.method == 'POST':
          if request.form['username'] != app.config['USERNAME']:
              error = 'Invalid username'
          elif request.form['password'] != app.config['PASSWORD']:
              error = 'Invalid password'
          else:
              session['logged_in'] = True
              flash('You were logged in')
              return redirect(url_for('index'))
      return render_template('login.html', error=error)


  @app.route('/logout')
  def logout():
      """User logout/authentication/session management."""
      session.pop('logged_in', None)
      flash('You were logged out')
      return redirect(url_for('index'))
  ```

  In the above `login()` function, the decorator indicates that the route can accept either a GET or POST request. Put simply, a request is initiated by the end user when they access the `/login` url. The difference between these requests is simple - GET is used for simply accessing a webpage, while POST is used when information is sent to the server. Thus, when a user simply accesses the `/login` url, they are using a GET request, but when they attempt to login, a POST request is used.

1. Add the template, "login.html":

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <title>Flaskr-TDD | Login</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>

    <div class="page">

      <h1>Flaskr</h1>
      <div class="metanav">
        {% if not session.logged_in %}
          <a href="{{ url_for('login') }}">log in</a>
        {% else %}
          <a href="{{ url_for('logout') }}">log out</a>
        {% endif %}
      </div>
      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}
      {% block body %}{% endblock %}

      <h2>Login</h2>
      {% if error %}
        <p class="error"><strong>Error:</strong> {{ error }}</p>
      {% endif %}
      <form action="{{ url_for('login') }}" method="post">
        <dl>
          <dt>Username:</dt>
          <dd><input type="text" name="username"></dd>
          <dt>Password:</dt>
          <dd><input type="password" name="password"></dd>
          <dd><input type="submit" value="Login"></dd>
        </dl>
      </form>

    </div>

  </body>
  </html>
  ```

1. Run the tests again.

  You should still see some errors! Look at one of the errors - `werkzeug.routing.BuildError: Could not build url for endpoint 'index'. Did you mean 'login' instead?`

  Essentially, we are trying to redirect to the `index()` function, which does not exist. Rename the `show_entries()` function to `index()` within *app.py* then re-test:

  ```sh
  Ran 5 tests in 0.070s

  FAILED (failures=1, errors=2)
  ```

1. Next, add in a View for adding entries:

  ```python
  @app.route('/add', methods=['POST'])
  def add_entry():
      """Add new post to database."""
      if not session.get('logged_in'):
          abort(401)
      db = get_db()
      db.execute(
          'insert into entries (title, text) values (?, ?)',
          [request.form['title'], request.form['text']]
      )
      db.commit()
      flash('New entry was successfully posted')
      return redirect(url_for('index'))
  ```

1. Retest.

  Now you should see:

  ```sh
  ======================================================================
  FAIL: test_empty_db (__main__.FlaskrTestCase)
  Ensure database is blank
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "app-test.py", line 49, in test_empty_db
      assert b'No entries here so far' in rv.data
  AssertionError

  ----------------------------------------------------------------------
  Ran 5 tests in 0.072s

  FAILED (failures=1)
  ```

  This error is asserting that when the route `/` is hit, the message "No entries here so far" is returned. Check the *index.html* Template. The message actually reads "No entries yet. Add some!". So update the test and then retest:

  ```sh
  Ran 5 tests in 0.156s

  OK
  ```

  Perfect.

## Add Some Color

Save the following styles to a new file called *style.css* in the "static" folder:

```css
body {
  font-family: sans-serif;
  background: #eee;
}

a, h1, h2 {
  color: #377BA8;
}

h1, h2 {
  font-family: 'Georgia', serif;
  margin: 0;
}

h1 {
  border-bottom: 2px solid #eee;
}

h2 {
  font-size: 1.2em;
}

.page {
  margin: 2em auto;
  width: 35em;
  border: 5px solid #ccc;
  padding: 0.8em;
  background: white;
}

.entries {
  list-style: none;
  margin: 0;
  padding: 0;
}

.entries li {
  margin: 0.8em 1.2em;
}

.entries li h2 {
  margin-left: -1em;
}

.add-entry {
  font-size: 0.9em;
  border-bottom: 1px solid #ccc;
}

.add-entry dl {
  font-weight: bold;
}

.metanav {
  text-align: right;
  font-size: 0.8em;
  padding: 0.3em;
  margin-bottom: 1em;
  background: #fafafa;
}

.flash {
  background: #CEE5F5;
  padding: 0.5em;
  border: 1px solid #AACBE2;
}

.error {
  background: #F0D6D6;
  padding: 0.5em;
}
```

## Test

Run you app, log in (username/password = "admin"), post, log out. Then run your tests to ensure that they still pass.

## jQuery

Now let's add some jQuery to make the site slightly more interactive.

1. Open *index.html* and update the first `<li`> like so:

  ```html
  <li class="entry"><h2 id={{ entry.id }}>{{ entry.title }}</h2>{{ entry.text|safe }}</li>
  ```

  Now we can use jQuery to target each `<li`>. First, we need to add the following scripts to the document just before the closing body tag:

  ```html
  <script src="//code.jquery.com/jquery-1.10.2.min.js"></script>
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="{{url_for('static', filename='main.js') }}"></script>
  ```

1. Create a *main.js* file in your "static" directory and add the following code:

  ```javascript
  $(function() {

    console.log( "ready!" ); // sanity check

    $('.entry').on('click', function() {
      var entry = this;
      var post_id = $(this).find('h2').attr('id');
      $.ajax({
        type:'GET',
        url: '/delete' + '/' + post_id,
        context: entry,
        success:function(result) {
          if(result.status === 1) {
            $(this).remove();
            console.log(result);
          }
        }
      });
    });

  });
  ```

1. Add a new function in *app.py* to remove the post from the database:

  ```python
  @app.route('/delete/<post_id>', methods=['GET'])
  def delete_entry(post_id):
      '''Delete post from database'''
      result = {'status': 0, 'message': 'Error'}
      try:
          db = get_db()
          db.execute('delete from entries where id=' + post_id)
          db.commit()
          result = {'status': 1, 'message': "Post Deleted"}
      except Exception as e:
          result = {'status': 0, 'message': repr(e)}

      return jsonify(result)
  ```

1. Finally, add a new test:

  ```python
  def test_delete_message(self):
      """Ensure the messages are being deleted"""
      rv = self.app.get('/delete/1')
      data = json.loads((rv.data).decode('utf-8'))
      self.assertEqual(data['status'], 1)
  ```

  Make sure to add the following import as well - `import json`

  Manually test this out by running the server and adding two new entries. Click on one of them. It should be removed from the DOM as well as the database. Double check this.

  Then run your automated test suite. It should pass:

  ```sh
  $ python app-test.py
  ......
  ----------------------------------------------------------------------
  Ran 6 tests in 0.132s

  OK
  ```

## Deployment

With the app in a working-state, let's shift gears and deploy the app to [Heroku](https://www.heroku.com).

1. To do this, first sign up and then install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

1. Next, install a web server called [gunicorn](http://gunicorn.org/):

  ```sh
  (env)$ pip install gunicorn==19.7.1
  ```

1. Create a [Procfile](https://devcenter.heroku.com/articles/procfile) in the project root:

  ```sh
  (env)$ touch Procfile
  ```

  And add the following code:

  ```sh
  web: gunicorn app:app
  ```

1. Create a *requirements.txt* file to specify the external dependencies that need to be installed for the app to work:

  ```sh
  (env)$ pip freeze > requirements.txt
  ```

1. Create a *.gitignore* file:

  ```sh
  (env)$ touch .gitignore
  ```

  And include the following files and folders (so they are not included in version control):

  ```sh
  env
  *.pyc
  *.DS_Store
  __pycache__
  ```

1. Add a local Git repo:

  ```sh
  (env)$ git init
  (env)$ git add -A
  (env)$ git commit -m "initial"
  ```

1. Deploy to Heroku:

  ```sh
  (env)$ heroku create
  (env)$ git push heroku master
  (env)$ heroku open
  ```

## Test (again!)

Let's test this in the cloud. Run `heroku open` to open the app in the browser.

## Bootstrap

Let's update the styles with Bootstrap 3.

1. First, remove the *style.css* stylesheet from both *index.html* and *login.html*.Then add this stylesheet to both files:

  ```html
  <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  ```

  Now we have full access to all of the Bootstrap helper classes.

1. Replace the code in *login.html* with:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <title>Flaskr-TDD | Login</title>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  </head>
  <body>

    <div class="container">

      <h1>Flaskr</h1>

      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}

      <h3>Login</h3>

      {% if error %}<p class="error"><strong>Error:</strong> {{ error }}{% endif %}</p>
      <form action="{{ url_for('login') }}" method="post">
        <dl>
          <dt>Username:</dt>
          <dd><input type="text" name="username"></dd>
          <dt>Password:</dt>
          <dd><input type="password" name="password"></dd>
          <br><br>
          <dd><input type="submit" class="btn btn-default" value="Login"></dd>
          <span>Use "admin" for username and password</span>
        </dl>
      </form>

    </div>

    <script src="//code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="{{url_for('static', filename='main.js') }}"></script>

  </body>
  </html>
  ```

1. And replace the code in *index.html* with:

  ```html
  <!DOCTYPE html>
  <html>
  <head>
    <title>Flaskr</title>
    <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
  </head>
  <body>

    <div class="container">

      <h1>Flaskr-TDD</h1>

      {% if not session.logged_in %}
        <a href="{{ url_for('login') }}">log in</a>
      {% else %}
        <a href="{{ url_for('logout') }}">log out</a>
      {% endif %}

      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}

      {% if session.logged_in %}
        <form action="{{ url_for('add_entry') }}" method="post" class="add-entry">
          <dl>
            <dt>Title:</dt>
            <dd><input type="text" size="30" name="title"></dd>
            <dt>Text:</dt>
            <dd><textarea name="text" rows="5" cols="40"></textarea></dd>
            <br><br>
            <dd><input type="submit" class="btn btn-default" value="Share"></dd>
          </dl>
        </form>
      {% endif %}

      <br>

      <ul class="entries">
        {% for entry in entries %}
          <li class="entry"><h2 id={{ entry.id }}>{{ entry.title }}</h2>{{ entry.text|safe }}</li>
        {% else %}
          <li><em>No entries yet. Add some!</em></li>
        {% endfor %}
      </ul>

    </div>

    <script src="//code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="{{url_for('static', filename='main.js') }}"></script>

  </body>
  </html>
  ```

Check out your changes!

## SQLAlchemy

Let's upgrade to [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/), in order to better manage our database.

### Setup SQLAlchemy

1. Start by installing Flask-SQLAlchemy:

  ```sh
  $ pip install Flask-SQLAlchemy==2.1
  ```

1. Create a *create_db.py* file, then add the following code:

  ```python
  # create_db.py


  from app import db
  from models import Flaskr


  # create the database and the db table
  db.create_all()

  # commit the changes
  db.session.commit()
  ```

  This file will be used to create our new database. Go ahead and delete the old .db (*flaskr.db*) along with the *schema.sql* file.

1. Next add a *models.py* file, which will be used to generate the new schema:

  ```python
  from app import db


  class Flaskr(db.Model):

      __tablename__ = "flaskr"

      post_id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String, nullable=False)
      text = db.Column(db.String, nullable=False)

      def __init__(self, title, text):
          self.title = title
          self.text = text

      def __repr__(self):
          return '<title {}>'.format(self.body)
  ```

### Update *app.py*

```python
# imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models


@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


if __name__ == '__main__':
    app.run()
```

Notice the changes in the config at the top, as well the means in which we're now accessing and manipulating the database in each view function - via SQLAlchemy instead of vanilla SQL.

### Create the DB

Run the following command to create the initial database:

```sh
(env)$ python create_db.py
```

### Update *index.html*

Update this line:

```python
<li class="entry"><h2 id={{ entry.post_id }}>{{ entry.title }}</h2>{{ entry.text|safe }}</li>
```

Pay attention to the `post_id`. Check the database to ensure that there is a matching field.

### Tests

Finally, update the tests:

```python
import unittest
import os
from flask import json

from app import app, db

TEST_DB = 'test.db'


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        """initial test. ensure that the database exists"""
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    # assert functions

    def test_empty_db(self):
        """Ensure database is blank"""
        rv = self.app.get('/')
        self.assertIn(b'No entries yet. Add some!', rv.data)

    def test_login_logout(self):
        """Test login and logout using helper functions"""
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        self.assertIn(b'You were logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You were logged out', rv.data)
        rv = self.login(app.config['USERNAME'] + 'x', app.config['PASSWORD'])
        self.assertIn(b'Invalid username', rv.data)
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'] + 'x')
        self.assertIn(b'Invalid password', rv.data)

    def test_messages(self):
        """Ensure that user can post messages"""
        self.login(app.config['USERNAME'], app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        self.assertNotIn(b'No entries here so far', rv.data)
        self.assertIn(b'&lt;Hello&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> allowed here', rv.data)

    def test_delete_message(self):
        """Ensure the messages are being deleted"""
        rv = self.app.get('/delete/1')
        data = json.loads(rv.data)
        self.assertEqual(data['status'], 1)


if __name__ == '__main__':
    unittest.main()
```

We've mostly just updated the `setUp()` and `tearDown()` methods.

Run the tests, and then manually test it by running the server and logging in and out, adding new entries, and deleting old entries.

If all is well, update your requirements (`pip  freeze > requirements.txt`) commit your code, then PUSH the new version to Heroku!

## Conclusion

1. Want my code? Grab it [here](https://github.com/mjhea0/flaskr-tdd).
1. View my app on [Heroku](http://flaskr-tdd.herokuapp.com/). Cheers!
1. Want more Flask fun? Check out [Real Python](http://www.realpython.com).
1. Want something else added to this tutorial? Add an issue to the repo. Cheers!
