import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import random
from settings import DB_NAME, DB_USER, DB_PASSWORD

database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, 'localhost:5432', DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        for category in Category.query.all():
            db.session.delete(category)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

    @classmethod
    def get_questions_by_category_id(cls, category_id):
        if category_id:
            questions = list(map(lambda question: question.format(),
                                 Question.query.filter(Question.category == category_id).all())) or []
        else:
            questions = []
        return questions

    @classmethod
    def get_questions(cls):
        return list(map(lambda question: question.format(), Question.query.all()))
    @classmethod
    def get_question_by_id(cls, question_id):
        if question_id:
            return Question.query.get(question_id)
        else:
            return None
    @classmethod
    def search_question_by_term(cls, term):
        return list(map(lambda question: question.format(),
                        Question.query.filter(Question.question.ilike('%' + term + '%')).all()))

    @classmethod
    def get_random_question(cls, previous_questions, quiz_category):
        fetched_questions = Question.query.filter(
                                Question.id.notin_([pq for pq in previous_questions]),
                                Question.category == quiz_category.get('id'))

        questions = list(map(lambda question: question.format(), fetched_questions)) or []
        if len(questions) != 0:
            return random.choice(questions)
        else:
            return False


    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }

    @classmethod
    def get_categories(cls):
        return list(map(lambda category: category.format(), Category.query.all()))

    @classmethod
    def get_category_by_id(cls, category_id):
        category = category_id and Category.query.get(category_id) or None
        if category:
            return category.format()
        else:
            return None

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        for category in Category.query.all():
            db.session.delete(category)
        db.session.commit()