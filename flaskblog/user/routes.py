from flask import render_template, url_for, flash, redirect, request, Blueprint
from datetime import date, datetime
from flaskblog.user.forms import (Registrationform, Loginform, 
                                Userupdateform, ResetEmailform, Resetpasswordform)
from flask_login import current_user, login_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog import bcrypt, db
from flaskblog.main.utils import save_pic
from flaskblog.user.utils import send_email

users = Blueprint('users', __name__)




@users.route('/registration', methods = ['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Registrationform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.profile_pic.data:
            pic_name=save_pic(form.profile_pic.data, "profile_pics") #-->Calling a function to save picture if any
            user = User(username = form.username.data, email = form.email.data, password = hashed_password, image = pic_name)
        else:
            user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()    
        flash('Your Account has been sucesfully registered', 'success')
        return  redirect(url_for('users.login'))
    return render_template('registration.html', form = form)

# Route for login
@users.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been sucessfully logged in', 'success')
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.home'))
        else:
            flash("Your crediantials are incorrect", "danger")    
    return render_template('login.html', form = form)    


@users.route('/user/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user = user)


# User update route
@users.route('/user/updateprofile', methods = ['GET', 'POST'])
@login_required
def updateprofile():
    user = current_user
    form = Userupdateform()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.profile_pic.data:
            pic_name = save_pic(form.profile_pic.data, "profile_pics")
            user.image = pic_name
            db.session.commit()
            flash("Your profile picture has been sucessfully updated", "sucess")
            return redirect(url_for('users.profile'))
        else:
            db.session.commit()
            flash("Your profile picture has been sucessfully updated", "success")
            return redirect(url_for('users.profile'))
    elif request.method == "GET":    
        form.username.data = user.username
        form.email.data = user.email
    return render_template('userupdate.html', form = form, user = user)



@users.route('/reset_password')
def resetrequest():
    if current_user.is_authenticated:
        return redirect('main.home')

    form =  ResetEmailform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_email(user)
        flash("An email has been sent to Mail Address", "info")
        return redirect ('users.login')
    return render_template('reset_email.html', form = form)    


# Route for resetting the password
@users.route('/reset_password/<token>')
def resetpasswordrequest(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.validate_token(token)
    if user is None:
        flash('Your token is either invalid or expired.', 'info')
        return redirect('users.resetrequest')

    form = Resetpasswordform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been successfully reset', 'success')
        return redirect('users.login')
    return render_template('reset_password.html', form = form)    


# Route for displaying the posts of invividual user
@users.route('/user/<string:uname>/posts')
def userposts(uname):
    user = User.query.filter_by(username = uname).first()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author = user)\
            .paginate(per_page=1, page=page)
    return render_template('userposts.html', posts = posts, title = f'Post of {uname}',username = uname)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))