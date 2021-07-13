from flask import Flask, url_for, render_template, \
    request, redirect, flash, make_response, send_from_directory,\
        abort
#from flask_bcrypt import Bcrypt
from database.db import initialize_db
from flask_restful import Api
from resources.route import initialize_routes
from markupsafe import escape
import os

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY']='myProject'
username = "test"
password = "test"
app.config['MONGODB_SETTINGS'] ={
    'host':'mongodb://'+username+':'+password+'@182.252.132.39/test'#+ '/?authSource=admin'
}
initialize_db(app)
initialize_routes(api)

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/getCookie')
def getCookie():
    username = request.cookies.get('username')
    return str(username)
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

@app.route('/cookie')
def setCookie():
    resp = make_response(render_template('hello.html'))
    resp.headers['X-Something'] = 'A value'
    resp.set_cookie('username', 'the username')
    return resp

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

# @app.route("/hello/<name>")
# def hello(name):
#     return f"Hello,{escape(name)}!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

from werkzeug.utils import secure_filename
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file_all():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/downloads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


with app.test_request_context():
    #print(url_for('index'))
    #print(url_for('login'))
    #print(url_for('login', next='jon', age=30))
    #print(url_for('profile', username='John'))
    print(url_for('static', filename='style.css'))

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

if __name__=="__main__":
    app.run(debug=True)
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')