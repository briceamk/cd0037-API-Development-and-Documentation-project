# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## End Points

#### `GET '/categories'`

- Fetches all `categories` in database. A `category` has the following attributes:
  - `id`: id of the category
  - `type`: name of the category
- Request Arguments: None
- Returns: a json with following key:
  - `categories`: array of Category
  - `success`: a boolean to prevent if operation has fail or successfully done.

```json
{
  "success": "True",
  "categories": [
    {
      "id": "1",
      "type": "Sport"
    },
    {
      "id": "2",
      "type": "Art"
    }
  ]
}
```

#### `GET '/questions'`

- Fetches all `questions` in database. A `question` has the following attributes:
  - `id`: id of the question
  - `category`: id of the category
  - `question`: the question
  - `answer`: answer of the question
  - `difficulty`: complexity of the question
- Request Arguments: 
  - `page`: page number to be fetched. a page ca have a maximum of 10 elements. It's nor required.
- Returns: a json with the following keys:
  - `categories`: array of Category
  - `success`: a boolean to prevent if operation has fail or successfully done.
  - `questions`: array of Question 
  - `current_category`: current category
  - `total_questions`: number of questions from database

```json
{
  "success": "True",
  "questions": [
    {
      "id": "1",
      "category": "4",
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "answer": "Apollo 13",
      "difficulty": "3"
    },
    {
      "id": "2",
      "category": "3",
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", 
      "answer": "Tom Cruise",
      "difficulty": "2"
    }
  ],
  "categories": [
    {
      "id": "1",
      "type": "Sport"
    },
    {
      "id": "2",
      "type": "Art"
    }
  ],
  "current_category": {
      "id": "1",
      "type": "Sport"
    },
  "total_questions": 15
}
```

#### `DELETE '/questions/<question_id>'`

- Delete a question by the `id` in database.
  - `id`: id of the category
  - `type`: name of the category
- Path parameter:
  - `id`: id of the question
- Returns: a json with following key:
  - `message`: inform that operation has successfully done
  - `success`: a boolean to prevent if operation has fail or successfully done.

```json
{
  "success": "True",
  "message": "Question with id 10 has  deleted successfully"
}
```

#### `POST '/questions'`

- Save a `question` in database. A `question` has the following attributes:
  - `id`: id of the question
  - `category`: id of the category
  - `question`: the question
  - `answer`: answer of the question
  - `difficulty`: complexity of the question
- Request body: 
  - `category`: id of the category. required
  - `question`: the question. required
  - `answer`: answer of the question. required
  - `difficulty`: complexity of the question. required
- Returns: a json with the following keys:
  - `categories`: array of Category
  - `success`: a boolean to prevent if operation has fail or successfully done.
  - `questions`: array of Question 
  - `current_category`: current category
  - `total_questions`: number of questions from database

```json
{
  "success": "True",
  "message": "Question created successfully"
}
```

#### `POST '/questions/search'`

- Search `questions` from database with a `searchTerm`. A `question` has the following attributes:
  - `id`: id of the question
  - `category`: id of the category
  - `question`: the question
  - `answer`: answer of the question
  - `difficulty`: complexity of the question
- Request body: 
  - `searchTerm`: keyword use to search question from database. required
- Returns: a json with the following keys:
  - `success`: a boolean to prevent if operation has fail or successfully done.
  - `questions`: array of Question 
  - `current_category`: current category
  - `total_questions`: number of questions fetched from database with the `searchTerm`

```json
{
  "success": "True",
  "questions": [
    {
      "id": "1",
      "category": "4",
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "answer": "Apollo 13",
      "difficulty": "3"
    },
    {
      "id": "2",
      "category": "3",
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", 
      "answer": "Tom Cruise",
      "difficulty": "2"
    }
  ],
  "total_questions": 8
}
```

#### `GET '/categories/<category_id>/questions'`

- Fetches all `questions` of specific `category_id` from database. A `question` has the following attributes:
  - `id`: id of the question
  - `category`: id of the category
  - `question`: the question
  - `answer`: answer of the question
  - `difficulty`: complexity of the question
- Path param: 
  - `catagory_id`: category `id` of questions to fetch from database
- Returns: a json with the following keys:
  - `success`: a boolean to prevent if operation has fail or successfully done.
  - `questions`: array of Question 
  - `current_category`: current category
  - `total_questions`: number of questions from database

```json
{
  "success": "True",
  "questions": [
    {
      "id": "1",
      "category": "4",
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "answer": "Apollo 13",
      "difficulty": "3"
    },
    {
      "id": "2",
      "category": "3",
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", 
      "answer": "Tom Cruise",
      "difficulty": "2"
    }
  ],
  "current_category": {
      "id": "1",
      "type": "Sport"
    },
  "total_questions": 15
}
```


#### `POST '/quizzes'`

- Search randomly one `question` of given `category` from database. A `question` has the following attributes:
  - `id`: id of the question
  - `category`: id of the category
  - `question`: the question
  - `answer`: answer of the question
  - `difficulty`: complexity of the question
- Request body: 
  - `previous_questions`: array of previous question fetched from database
  - `quiz_category`: category by where question will be fetched
- Returns: a json with the following keys:
  - `question`: question fetched from database 
```json
{
  "question": {
      "id": "1",
      "category": "4",
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "answer": "Apollo 13",
      "difficulty": "3"
    }
}
```

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
