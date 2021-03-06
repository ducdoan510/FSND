# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetch paginated list of questions
- Request Arguments: page
- Returns: A dictionary contains all questions, the dictionary contains following keys: success, quetions, total_questions, categories, current_category
{
    "success": True,
    "questions": [{"id": "1", "question": "What is it?", "answer": "A pen", "category": "1", "difficulty": 1}],
    "total_questions": 2
    "categories": {'1': "Sciences'}
    "current_categories": null
}

POST '/questions'
- Create a new question
- Post data: must have the following keys: question, answer, category, difficulty
- Returns: A list of questions including the newly created questions. The format is same as as json returned by GET /questions
{
    "success": True,
    "questions": [{"id": "1", "question": "What is it?", "answer": "A pen", "category": "1", "difficulty": 1}],
    "total_questions": 2
    "categories": {'1': "Sciences'}
    "current_categories": null
}


DELETE '/questions/<question_id>'
- Delete the question with specified id

POST '/questions'
- Search quetions by search term
- Post data: must have the key: searchTerm
- Returns: A list of questions of same format as GET '/questions' where any question has the searchTerm in its question
{
    "success": True,
    "questions": [{"id": "1", "question": "What is it?", "answer": "A pen", "category": "1", "difficulty": 1}],
    "total_questions": 2
    "categories": {'1': "Sciences'}
    "current_categories": null
}

GET '/categories/<category_id>/questions'
- Get all questions that belong to a certain category (specified by category_id in the request URL)
- Parameters: page
- Returns: A list of questions that belong to a specified category. The format is same as result of GET '/questions'
{
    "success": True,
    "questions": [{"id": "1", "question": "What is it?", "answer": "A pen", "category": "1", "difficulty": 1}],
    "total_questions": 2
    "categories": {'1': "Sciences'}
    "current_categories": null
}

POST '/quizzes'
- Get a question for the next quiz
- Post data: must have the following keys: previous questions, quiz_category
- Returns: A question that did not appear in previous questions and belong to quiz category
{
    "quetions": {"id": "1", "question": "What is it?", "answer": "A pen", "category": "1", "difficulty": 1}
}


## Error code
This project will return the following HTTP Errors

404: Not found
- When page does not exist (e.g. paginated page of questions that is more than the number of actual questions)
- Returns: 
{
    "success": false,
    "error": 404,
    "message": "Not found"
}

400: Bad Request
- When user request is invalid or wrongly formatted
- Returns:
{
    "success": false,
    "error": 422,
    "message": "Not found"
}

422: Unprocessable request
- When user request is syntactically valid but the server cannot process with the request
- Returns:
{
    "success": False,
    "error": 422,
    "message": 'Unprocessable request'
}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
