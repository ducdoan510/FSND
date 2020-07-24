import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
import logging
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(objs, page, page_size=QUESTIONS_PER_PAGE):
    start = (page - 1) * page_size
    return objs[start: start + page_size]


def get_formatted_question(questions, page=None):
    formatted_questions = [q.format() for q in questions]
    if page is None:
        paginated_questions = formatted_questions
    else:
        paginated_questions = paginate(formatted_questions, page)
    return len(formatted_questions), paginated_questions


def get_category_map():
    categories = Category.query.all()
    category_json = {}
    for cat in categories:
        category_json[cat.id] = cat.type
    return category_json


def list_questions_response(questions, page, current_category):
    total_questions, paginated_questions = get_formatted_question(questions, page)

    if not paginated_questions:
        abort(404)

    # build categories map
    category_json = get_category_map()

    return jsonify({
        "success": True,
        'questions': paginated_questions,
        'total_questions': total_questions,
        'categories': category_json,
        'current_category': current_category
    })


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        category_json = {}
        for cat in categories:
            category_json[cat.id] = cat.type
        return jsonify({'categories': category_json})

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        return get_questions_by_category(None)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(400)
            db.session.delete(question)
            db.session.commit()
        except Exception as e:
            logging.error(str(e))
            db.session.rollback()
            abort(400)
        finally:
            db.session.close()
        return jsonify({
            "success": True
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            if request.json.get('searchTerm', None) is not None:
                return search_question()
            question = Question(**request.json)
            db.session.add(question)
            db.session.commit()
        except Exception as e:
            logging.error(str(e))
            abort(400)
        finally:
            db.session.close()
        return get_questions()

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions', methods=['POST'])
    def search_question():
        search_term = request.json['searchTerm']
        questions = Question.query.filter(Question.question.contains(search_term)).order_by(Question.id).all()
        return list_questions_response(questions, 1, None)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)

        # get filtered questions
        current_category = Category.query.get(category_id).format() if category_id else None
        question_filter_query = Question.query.filter_by(category=category_id) if category_id else Question.query
        questions = question_filter_query.order_by(Question.id).all()

        return list_questions_response(questions, page, current_category)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        previous_questions = request.json['previous_questions']
        quiz_category = request.json['quiz_category']
        category = Category.query.get(quiz_category['id'])
        if not category:
            questions = Question.query
        else:
            questions = Question.query.filter_by(category=quiz_category['id'])
        questions = questions.filter(Question.id.notin_(previous_questions))
        total, formatted_questions = get_formatted_question(questions)

        random_question_idx = random.randint(0, total - 1) if total > 0 else None
        random_question = formatted_questions[random_question_idx] if random_question_idx is not None else None
        return jsonify({
            'question': random_question
        })

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad request'
        }), 400

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable request'
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
