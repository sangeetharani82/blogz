from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True


form = """
<!doctype html>
<html>
    <h1>Add a Blog Entry</h1>
    <body>
        <form action="/blog", style="font-size:13px", method="post">
            <label>Title for your new blog:
                <br><input type="text" name="blog_title" /> 
            </label><br>
            <label>Your New Blog:
                <br><textarea type="text" name="new_blog"></textarea>
            </label><br><br>
                <input type="submit" value="Add Entry" />
            
        </form>
    </body>
</html>
"""

@app.route("/")
def index():
    return form

@app.route("/blog", methods=['POST'])
def blog():
    blog_title = request.form['blog_title']
    new_blog = request.form['new_blog']
    return '<h4>' + blog_title + '</h4>' + new_blog

app.run()