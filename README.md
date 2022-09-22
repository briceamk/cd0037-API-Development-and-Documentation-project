# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


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