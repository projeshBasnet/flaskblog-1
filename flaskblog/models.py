from flaskblog import db
from datetime import datetime
from flaskblog import login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creating a models 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(70), nullable = False)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(60), default = "bg1.jpg")
    posts = db.relationship('Post', backref='author', lazy = True)

    def __repr__(self):
        return f"(Username: {self.username}), (email: {self.email}), (image: {self.image})"

    def get_reset_token(self, expiry_time = 1800):
        s = serializer(app.config['SECRET_KEY'],expiry_time)
        return s.dumps({user_id: self.id}).decode('utf-8')

    @staticmethod
    def validate_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)        





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable = False, unique = True)
    content = db.Column(db.Text, nullable = False)
    dateposted = db.Column(db.DateTime, default = datetime.utcnow)
    genere = db.Column(db.String(50), default = "others")
    image = db.Column(db.String(60),   default = "blog1.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"(Title: {self.title}),  (Genere : {self.genere})"