# Trivia API

**_this backend flask ( python ) server provides restful apis for frontend react.js application to make requests that provides and sends questions_**

1. **_Clone the repository:_** `git clone git@github.com:MAMOUN-kamal-alshisani/TriviaAPI.git`

2. **_Install dependencies:_** `npm install`

3. **Set up environment variables: Create a `.env` file and add the following variables:** -`DB_HOST`:'Database host' -`DB_USER`:'Database username' -`DB_PASSWORD`:'Database password'

4. **_Start the server:_** -`export FLASK_ENV=development` -`export FLASK_APP=flaskr` -`flask run`

5. **_Start the react.js client app:_** -`npm start`

   **_if an error message is displayed when running `npm start command, try running:`_** -`export NODE_OPTIONS=--openssl-legacy-provider` -`npm start`

## API Endpoints

### GET /api/categories

Returns a list of all categories.

#### Request

- Method: GET
- Endpoint: `/api/categories`

#### Response

- Status: 200 OK
- Body:

**_{
id:1,
type:"travel"
}_**

### GET /api/questions

Returns a list of all Questions.

#### /api/questions Request

- Method: GET
- Endpoint: `/api/questions`

#### /api/questions Response

- Status: 200 OK
- Body:

_data ={
"success":True,
"categories":category,
"total_questions":len(questions),
"current_category":None,
"questions":currQuestions
}_

### DELETE /api/question/<int:question_id>

DELETE a Question that matches the id.

#### /api/question/<int:question_id> Request

- Method: DELETE
- Endpoint: `/api/question/1`

#### /api/question/<int:question_id> Response

- Status: 200 OK
- Body:

_{
"success":True,
"message":'question with id {question_id} has been removed successfully!',
}_

### POST /api/question

Creates a new question.

#### /api/question Request

- Method: POST
- Endpoint: `/api/question`
- Body:
  {
  "success":True,
  "message":'question has been created successfully!',
  }

### POST /api/questions/search

searches in questions list for any question that matches the input .

#### /api/questions/search Request

- Method: POST
- Endpoint: `/api/questions/search`
- Body:
  {
  searchTerm: 'word'
  }

### GET /api/categories/<int:category_id>/questions

get questions based on category.

#### /api/categories/<int:category_id>/questions Request

- Method: GET
- Endpoint: `/api/categories/1/questions`

#### /api/question/<int:question_id> RESPONSE

- Endpoint: `/api/question/1`
- Body:
  _{
  'success': True,
  'questions': question,
  'total_questions': len(question),
  'current_category': category_id
  }_
