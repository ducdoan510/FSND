import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import json
import pprint


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        expected_res = {'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'}}
        self.assertEqual(json.loads(res.data), expected_res)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_not_exists_page(self):
        res = self.client().get('/questions?page=100')
        self.assertEqual(res.status_code, 404)

    def test_create_and_delete_question(self):
        # test create new question
        client = self.client()
        res = client.post('/questions', json={'question': 'To be or not to be?', 'answer': 'To be', 'category': 6, 'difficulty': 1})
        self.assertEqual(res.status_code, 200)

        # test delete question
        question = Question.query.filter_by(question='To be or not to be?').first()
        res = client.delete(f'/questions/{question.id}')
        self.assertEqual(res.status_code, 200)

    def test_delete_invalid_question(self):
        res = self.client().delete('/questions/0')
        self.assertEqual(res.status_code, 400)

    def test_search_question(self):
        term = 'What'
        res = self.client().post('/questions', json={'searchTerm': term})
        self.assertEqual(res.status_code, 200)
        questions = json.loads(res.data)['questions']
        for question in questions:
            assert term in question['question']

    def test_get_questions_by_category(self):
        category = 5
        res = self.client().get(f'/categories/{category}/questions')
        self.assertEqual(res.status_code, 200)
        questions = json.loads(res.data)['questions']
        for q in questions:
            self.assertEqual(q['category'], category)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
