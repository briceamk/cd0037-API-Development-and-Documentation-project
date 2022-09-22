
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from datetime import datetime


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        return jsonify({
            'success': True,
            'categories': Category.get_categories(),

        }), 200

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        categories = Category.get_categories()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', QUESTIONS_PER_PAGE, type=int)
        start = (page - 1) * size
        end = start + size
        questions = Question.get_questions()
        return jsonify({
            'success': True,
            'questions': questions[start:end],
            'current_category': categories[0],
            'categories': categories,
            'total_questions': len(questions)
        }), 200

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_by_id(question_id):
        question = Question.get_question_by_id(question_id)
        if not question:
            abort(404, 'Question with id {} not found'.format(question_id))
        try:
            question.delete()
            return jsonify({
                'success': True,
                'message': 'Question with id {} deleted successfully'.format(question_id)
            }), 200
        except Exception as e:
            abort(500, 'Unknown server error ')

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        question = request.get_json()
        errors = []
        if 'question' not in question:
            errors.append({'field': 'question', 'message': 'question is required'})
        if 'answer' not in question:
            errors.append({'field': 'answer', 'message': 'answer is required'})
        if 'category' not in question:
            errors.append({'field': 'category', 'message': 'category is required'})
        if 'difficulty' not in question:
            errors.append({'field': 'difficulty', 'message': 'difficulty is required'})
        if errors:
            abort(400, errors)
        if question.get('category'):
            category = Category.get_category_by_id(question.get('category'))
            if not category:
                abort(404, 'Category with id {} not found'.format(question.get('category')))
        try:
            question = Question(**question)
            question.insert()
            return jsonify({
                'success': True,
                'message': 'Question created successfully'
            }), 201
        except Exception as e:
            print(e)
            abort(500, 'Unknown server error')

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions_by_term():
        keyword = request.get_json()
        if keyword and 'searchTerm' in keyword:
            questions = Question.search_question_by_term(keyword.get('searchTerm'))
            return jsonify({
                'success': True,
                'questions': questions,
                'totalQuestions': len(questions)
            }), 200
        else:
            abort(400, [{'field': 'term', 'message': 'term to search is required'}])


    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.get_category_by_id(category_id)
        if not category:
            abort(404, 'Category with id {} not found'.format(category_id))
        questions = Question.get_questions_by_category_id(category_id)
        return jsonify({
            'success': True,
            'currentCategory': category,
            'questions': questions,
            'totalQuestions': len(questions)
        }), 200

    """
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        data = request.get_json()
        if 'previous_questions' not in data:
            data.update({'previous_questions': []})
        if 'quiz_category' not in data:
            abort(400, 'Quiz category is required')
        current_question = Question.get_random_question(data.get('previous_questions'), data.get('quiz_category'))
        if current_question:
            return jsonify({
                'question': current_question
            })
        else:
            return jsonify({
                'question': False
            })

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': error.description or '',
            'timestamp': datetime.now(),
            'path': request.full_path or ''
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': error.description or '',
            'timestamp': datetime.now(),
            'path': request.full_path or ''
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description or '',
            'timestamp': datetime.now(),
            'path': request.full_path or ''
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': error.description or '',
            'timestamp': datetime.now(),
            'path': request.full_path or ''
        }), 500

    return app
