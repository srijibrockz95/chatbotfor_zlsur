from . import db
from sqlalchemy.sql import func


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userfname = db.Column(db.String(120), nullable=False)
    useremail = db.Column(db.String(120), nullable=False, unique=True)
    userid = db.Column(db.String(20), nullable=False, unique=True)
    userrole = db.Column(db.String(50), nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, userfname, useremail, userid, userrole, passwordhash, createdby):
        self.userfname = userfname
        self.useremail = useremail
        self.userid = userid
        self.userrole = userrole
        self.passwordhash = passwordhash
        self.createdby = createdby

    def __repr__(self):
        return '<Login %r>' % self.userfname


class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_type = db.Column(db.String(80), nullable=False)
    question = db.Column(db.String(240), nullable=False)
    answer = db.Column(db.String(240))
    relatedquesid = db.Column(db.Integer)
    orderofdisp = db.Column(db.Integer)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, question_type, question, answer, relatedquesid, orderofdisp, createdby):
        self.question_type = question_type
        self.question = question
        self.answer = answer
        self.relatedquesid = relatedquesid
        self.orderofdisp = orderofdisp
        self.createdby = createdby

    def __repr__(self):
        return '<QuestionAnswer %r>' % self.question


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(20), nullable=False)
    bookingmessage = db.Column(db.String(300), nullable=False)
    creationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updationdatetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    createdby = db.Column(db.String(20))
    modifiedby = db.Column(db.String(20))

    def __init__(self, userid, bookingmessage, createdby):
        self.userid = userid
        self.bookingmessage = bookingmessage
        self.createdby = createdby

    def __repr__(self):
        return '<Booking %r>' % self.userid
