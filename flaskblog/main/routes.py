from flask import render_template, Blueprint, request
from flaskblog import app
from datetime import date
from flaskblog.models import Post

main = Blueprint('main', __name__)




@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page = page, per_page = 1)
    return render_template('home.html', title = "Home Page", posts = posts)