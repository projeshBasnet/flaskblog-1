from flaskblog import mail
from flask import url_for
from flask_mail import Message

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Reset password form',sender='demouser@gmail.com', recipients=[user.email])
    msg.body=  f'''To reset your password please click to the link given below

{url_for('users.resetpasswordrequest', token = token, _external = True)}

If you didnot make any request ten please ignore it. No changes will be made

'''
    mail.send(msg)

