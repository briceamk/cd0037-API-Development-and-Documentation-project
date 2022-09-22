import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.username = 'flask'
        self.password = 'flask123'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.username, self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        categories = [
            {'type': 'Science'},
            {'type': 'Art'},
            {'type': 'Geography'},
            {'type': 'History'},
            {'type': 'Entertainment'},
            {'type': 'Sport'}
        ]
        questions = [
            {
                'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
                'answer': 'Apollo 13',
                'category': 4,
                'difficulty': 3
            },
            {
                'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved '
                            'Lestat?',
                'answer': 'Tom Cruise',
                'category': 3,
                'difficulty': 2
            },
            {
                'question': 'Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?',
                'answer': 'Maya Angelou',
                'category': 1,
                'difficulty': 5
            },
            {
                'question': 'WWhat boxer\'s original name is Cassius Clay?',
                'answer': 'Muhammad Ali',
                'category': 6,
                'difficulty': 3
            },
            {
                'question': 'Who invented Peanut Butter?',
                'answer': 'George Washington Carver',
                'category': 5,
                'difficulty': 1
            },
            {
                'question': 'Who discovered penicillin?',
                'answer': 'Alexander Fleming',
                'category': 5,
                'difficulty': 5
            }
        ]
        db_questions = Question.get_questions()
        db_categories = Category.get_categories()
        if len(db_categories) == 0:
            for category in categories:
                cat = Category(**category)
                cat.insert()
        if len(db_questions) == 0:
            for question in questions:
                quest = Question(**question)
                quest.insert()



    def tearDown(self):
        """Executed after reach test"""
        # Question.delete_all()
        # Category.delete_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(len(data.get('categories')), 6)

    def test_get_categories_fail(self):
        res = self.client().get('category')

        self.assertEqual(res.status_code, 404)

    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreaterEqual(data.get('total_questions'), 0)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('categories'))
        self.assertTrue(data.get('current_category'), data.get('categories')[0])

    def test_get_question_fail(self):
        res = self.client().get('/question')

        self.assertEqual(res.status_code, 404)

    def test_delete_question_by_id_success(self):
        # Given
        question = {
                'question': 'Who discovered penicillin?',
                'answer': 'Alexander Fleming',
                'category': 5,
                'difficulty': 5
        }
        quest = Question(**question)
        quest.insert()
        quests = Question.get_questions()
        question_id = quests[len(quests) - 1].get('id')

        # When
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        # Then
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('message'), 'Question with id {} deleted successfully'.format(question_id))
        self.assertTrue(data.get('success'))

    def test_delete_question_by_id_fail(self):

        #Given
        question_id = 10000

        #When
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        #Then
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('message'), 'Question with id {} not found'.format(question_id))
        self.assertFalse(data.get('success'))

    def test_create_question_success(self):
        question = {
            'question': 'Who was the first president of Cameroon?',
            'answer': 'Amadou Ahidjo',
            'category': 4,
            'difficulty': 5
        }

        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data.get('message'), 'Question created successfully')
        self.assertTrue(data.get('success'))

    def test_create_question_fail(self):
        question = {
            'question': 'Who was the first president of Cameroon?',
            'answer': 'Amadou Ahidjo',
            'difficulty': 5
        }

        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        message = data.get('message')[0].get('message')
        field = data.get('message')[0].get('field')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(message, 'category is required')
        self.assertEqual(field, 'category')
        self.assertFalse(data.get('success'))

    def test_search_term_success(self):
        keyword = {
            'searchTerm': 'who'
        }

        res = self.client().post('/questions/search', json=keyword)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('totalQuestions'))

    def test_search_term_fail(self):
        keyword = {
        }

        res = self.client().post('/questions/search', json=keyword)
        data = json.loads(res.data)

        message = data.get('message')[0].get('message')
        field = data.get('message')[0].get('field')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(message, 'term to search is required')
        self.assertEqual(field, 'term')
        self.assertFalse(data.get('success'))

    def test_get_questions_by_category_success(self):
        category_id = 5
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('currentCategory'))
        self.assertTrue(data.get('success'))

    def test_get_questions_by_category_fail(self):
        category_id = 200
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('message'), 'Category with id {} not found'.format(category_id))
        self.assertFalse(data.get('success'))

    def test_quizzes_success(self):
        quizz = {
            'previous_questions': [],
            'quiz_category': {
                'id': '5'
            }
        }

        res = self.client().post('/quizzes', json=quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('question'))

    def test_quizzes_fail(self):
        quizz = {
        }

        res = self.client().post('/quizzes', json=quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data.get('message'), 'Quiz category is required')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
