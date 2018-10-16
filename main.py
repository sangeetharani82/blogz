from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Amba26aug1956!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost')
def display_newpost_form():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST', 'GET'])
def validate_blog():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        posts = Post(blog_title, blog_body)
        db.session.add(posts)
        db.session.commit()

    blog_titles = Post.query.all()
    blog_bodyz = Post.query.all()

    title_error = ''
    body_error = ''

    if blog_title == '':
        title_error = "Please fill in the title"
        blog_title = ''

    if blog_body == '':
        body_error = "Please fill in the body"
        blog_body = '' 
    
    if not title_error and not body_error:
        return render_template('single_blog.html', blog_title=blog_title, blog_body=blog_body)
    else:
        return render_template('newpost.html', title_error=title_error, body_error=body_error, blog_title=blog_title, 
            blog_body=blog_body, blog_titles=blog_titles, blog_bodyz=blog_bodyz, page_title='Blogz')

@app.route("/blog", methods=['POST', 'GET'])
def main_blog():
    if request.args.get('id'):
        title_id = request.args.get('id')
        blogs = Post.query.get(title_id)
        blog_title = blogs.title
        blog_body = blogs.body 
        return render_template('single_blog.html', blog_title=blog_title, blog_body=blog_body)

    if not request.args.get('id'):
        blog_titles = Post.query.all()
        blog_bodyz = Post.query.all()
        return render_template('blog.html', blog_titles=blog_titles, page_title='Blogz', 
            blog_bodyz=blog_bodyz)

# ---------------------User/logn/signup------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':#empty fields
            flash('Invalid username', 'error')
            return redirect('/login')
        user = User.query.filter_by(username=username).first()
        if user and user.password != password:#pswd incorrect
            flash('Password is incorrect', 'error')
            return redirect('/login')
        if user and user.password == password: #validation succeeds
            session['username'] = username
            flash("Logged in", 'information')
            flash('Welcome back ' + username.capitalize() + '!', 'information')
            #print(session)
            return redirect('/newpost')
        elif not user:#new user
            flash('Username does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == '' or password == '' or verify == '':#empty fields
            flash('One or more fields are invalid', 'error')
            return redirect('/signup')
        if len(username) < 3:
            flash('Invalid username', 'error')
            return redirect('/signup')
        if len(password) < 3 or len(verify) < 3:
            flash('Invalid password', 'error')
            return redirect('/signup')
        else:
            if password != verify:#mismatch pswd
                flash("Password don't match", 'error')
                return redirect('/signup')
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:#new user
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            flash('Welcome to your blog, ' + username.capitalize() + '!', 'information')
            return redirect('/newpost')
        else:
            flash('Username already exists', 'error')#same username used to create one more account
            return redirect('/signup')

    return render_template('signup.html')

@app.route("/")
def index():
    blog_titles = Post.query.all()
    blog_bodyz = Post.query.all()
    return render_template('blog.html', blog_titles=blog_titles, page_title='Blogz', 
        blog_bodyz=blog_bodyz)


if __name__ == "__main__":
    app.run()