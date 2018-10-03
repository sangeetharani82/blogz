from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Amba26aug1956!@localhost:8889/build-a-blog'

@app.route("/newpost")
def display_post():
    return render_template('newpost.html')

blog_titles = []
blog_bodyz = []

@app.route('/newpost', methods=['POST', 'GET'])
def validate_post():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_titles.append(blog_title)
        blog_body = request.form['blog_body']
        blog_bodyz.append(blog_body)
        
    blog_posts = dict(zip(blog_titles, blog_bodyz))
    
    title_error = ''
    body_error = ''

    if blog_title == '':
        title_error = "Please fill in the title"
        blog_title = ''

    if blog_body == '':
        body_error = "Please fill in the body"
        blog_body = '' 
    
    if not title_error and not body_error:
        return render_template('blog.html', blog_posts=blog_posts)
    else:
        return render_template('newpost.html',title_error=title_error, 
            body_error=body_error, blog_title=blog_title, blog_body=blog_body, blog_posts=blog_posts)


@app.route("/blog", methods=['POST', 'GET'])
def blog():
    blog_posts = dict(zip(blog_titles, blog_bodyz))
    return render_template('blog.html', blog_posts=blog_posts)

@app.route("/individual_blog", methods=['POST', 'GET'])
def individual_blog():
    blog_posts = dict(zip(blog_titles, blog_bodyz))
    return render_template('individual_blog.html', blog_posts=blog_posts)

@app.route("/", methods=['POST', 'GET'])
def index():
   
    blog_posts = dict(zip(blog_titles, blog_bodyz))
    return render_template('base.html', blog_posts=blog_posts)


app.run()