from flask import Flask, request, redirect, render_template
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/newpost')
def display_newpost_form():
    return render_template('newpost.html')


@app.route("/newpost", methods=['POST'])
def validate_newpost():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']
    title_error = ''
    blog_error = ''

    if blog_title == '':
        title_error = "Please fill in the title"
        blog_title = ''

    if blog_body == '':
        blog_error = "Please fill in the body"
        blog_body = ''

    if not title_error and not blog_error:
        return '<h4>' + blog_title + '</h4>' + blog_body
    else:
        return render_template('newpost.html', title_error=title_error, blog_error=blog_error, 
            blog_title=blog_title, blog_body=blog_body)

blogpost = {}
blogtitle=[]
blogbody=[]

@app.route("/newpost", methods=['POST', 'GET'] )
def display_post():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blogtitle.append(blog_title)
        blog_body = request.form['blog_body']
        blogbody.append(blog_body)
    blogpost = dict(zip(blog_title, blog_body))
    return render_template("newpost.html", blogpost=blogpost)


@app.route("/blog", methods=['POST', 'GET'])
def blog():
    
    return render_template('blog.html', title="Blogz", blogpost=blogpost)

@app.route("/")
def index():
    return render_template('base.html')

app.run()