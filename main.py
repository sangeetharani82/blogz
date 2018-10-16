from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Amba26aug1956!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

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

# ---------------------User------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')

@app.route("/")
def index():
    blog_titles = Post.query.all()
    blog_bodyz = Post.query.all()
    return render_template('blog.html', blog_titles=blog_titles, page_title='Blogz', 
        blog_bodyz=blog_bodyz)


if __name__ == "__main__":
    app.run()