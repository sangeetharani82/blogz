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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/newpost')
def display_newpost_form():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST', 'GET'])
def validate_blog():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        posts = Post(blog_title, blog_body, owner)
        db.session.add(posts)
        db.session.commit()

    blog_titles = Post.query.filter_by(owner=owner).all()
    blog_bodyz = Post.query.filter_by(owner=owner).all()

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
        #owner = User.query.filter_by(username=session['username']).first()
        #blog_titles = Post.query.filter_by(owner=owner).all()
        #blog_bodyz = Post.query.filter_by(owner=owner).all()
        blog_titles = Post.query.all()
        blog_bodyz = Post.query.all()

        return render_template('blog.html', blog_titles=blog_titles, page_title='Blogz', 
            blog_bodyz=blog_bodyz)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('Invalid username', 'error')
            return redirect('/login')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in", 'information')
            flash('Welcome back ' + username + '!', 'information')
            print(session)
            return redirect('/newpost')
        elif user and user.password != password:
            flash('Password is incorrect', 'error')
            return redirect('/login')
        elif not user:
            flash('Username does not exist', 'error')
            return redirect('/login')                   

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if username == '' or password == '' or verify == '':
            flash('One or more fields are invalid', 'error')
            return redirect('/signup')
        if len(username) < 3:
            flash('Invalid username', 'error')
            return redirect('/signup')
        if len(password) < 3 or len(verify) < 3:
            flash('Invalid password', 'error')
            return redirect('/signup')
        else:
            if password != verify:
                flash("Password don't match", 'error')
                return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Welcome to your blog ' + username + '!', 'information')
            return redirect('/newpost')
        else:
            flash('Username already exists', 'error')
            return redirect('/signup')
      
   
    #if not name_error and not pswd_error and not v_pswd_error:
     #   return '<h1>Welcome' + username +'!</h1>'
#redirect /newpost
#any empty field,"one or more fields are invalid"
#(new)username already exists
#password dont match
#name and pswd < 3, invalid name or pswd
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route("/")
def index():
    #owner = User.query.filter_by(username=session['username']).first()
    #blog_titles = Post.query.filter_by(owner=owner).all()
    #blog_bodyz = Post.query.filter_by(owner=owner).all()
    blog_titles = Post.query.all()
    blog_bodyz = Post.query.all()

    return render_template('blog.html', blog_titles=blog_titles, page_title='Blogz', 
        blog_bodyz=blog_bodyz)


if __name__ == "__main__":
    app.run()