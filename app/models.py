from flask.ext.login import UserMixin
from app import db, lm

ROLE_USER=0;
ROLE_ADMIN=1;

@lm.user_loader
def get_user(ident):
  return User.query.get(int(ident))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r mail: %r >' % (self.nickname, self.email)
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)