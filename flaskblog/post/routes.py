from flaskblog import app
from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from flaskblog.post.forms import Createpost
from flaskblog.models import Post
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.main.utils import save_pic

posts = Blueprint('posts', __name__)


# Route for creating new post
@posts.route('/post/new', methods= ['GET', 'POST'])
@login_required
def createpost():
    form = Createpost()
    if form.validate_on_submit():
        post = Post(title = form.title.data, genere = form.genere.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been sucessfully posted", "success")
        return redirect(url_for('main.home'))
    return render_template('post.html', form = form)


@posts.route('/post/<int:post_id>')
def eachpost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('eachpost.html', post= post)


@posts.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        abort(403)
    form = Createpost()
    if form.validate_on_submit():
        if form.blog_pic.data:
            img_name=save_pic(form.blog_pic.data, "blog_pics")
        else:
            img_name = None
        post.title = form.title.data
        post.genere = form.genere.data
        post.content = form.content.data
        post.image = img_name
        db.session.commit()
        flash("Your post has been sucessfully updated ", "success")
        return redirect(url_for('main.home'))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.genere.data = post.genere
    return render_template('post.html', form = form)  
   
@posts.route('/post/<int:post_id>/delete')
@login_required
def deletepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        flash('Your donot have permission to delete this post', 'warnning')
        return redirect(url_for('main.home'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been sucessfully deleted', 'success')
    return redirect(url_for('main.home'))
     