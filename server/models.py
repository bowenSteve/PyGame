from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import re
from datetime import datetime

# Define metadata with naming conventions
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize db and bcrypt
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    scores = db.relationship('Score', back_populates='user')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required.')
        return name

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError(f'Invalid email address: {email}')
        return email

    def __repr__(self):
        return f'<User {self.name}, {self.email}>'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    scores = db.relationship('Score', back_populates='quiz')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [question.to_dict() for question in self.questions]
        }

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'choices': [choice.to_dict() for choice in self.choices]
        }

class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'is_correct': self.is_correct
        }

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    quiz_id = db.Column(db.Integer, ForeignKey('quizzes.id'))
    score = db.Column(db.Integer, nullable=False)  # Add this line to store the score

    user = db.relationship('User', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')

    serialize_rules = ('-user.scores', '-quiz.scores',)

class BlacklistedToken(db.Model):
    __tablename__ = 'blacklisted_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlacklistedToken {self.token}>'
