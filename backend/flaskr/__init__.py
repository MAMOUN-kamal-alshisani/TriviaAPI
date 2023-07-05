import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category,db
from dotenv import load_dotenv
load_dotenv()

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": ['*']}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers','Content-Type','Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories')
    def handle_categories():
           fetch_categories = Category.query.all()
           category = {category.id: category.type for category in fetch_categories}
          #  category = {category.format() for category in fetch_categories}

           if len(category) != 0:
                
            return jsonify({
              'success':True,
              'categories':category,
              'total_categories' : len(category)
        })
           else:
             return jsonify({
              'success':False,
              'categories':{},
              'total_categories' : 0
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/questions')
    def handle_questions():
      
      try:

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE         

        questions = Question.query.all()
        question = [question.format() for question in questions]
        currQuestions = question[start:end]

        fetch_categories = Category.query.all()
        category = {category.id: category.type for category in fetch_categories}
        
        # [category.format() for category in fetch_categories]
        
        if len(category) != 0:
          data =    {
            "success":True,
            "categories":category,
            "total_questions":len(questions),
            "current_category":None,
            "questions":currQuestions
                      }
          
          return jsonify(data)
          
        else:
            data =    {
            "success":False,
            "categories":[],
            "total_questions":len(questions),
            "current_category":None,
            "questions":currQuestions
                      }
            
            return jsonify(data)
        
      except Exception as e:
                print(e)
                abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/question/<int:question_id>', methods = ['DELETE'])
    def handle_question_removal(question_id):
         try:
           
           question_record = Question.query.get(question_id)
           question_record.delete()
           db.session.commit()

           if(question_record != None):
                
              data =    {
               "success":True,
               "message": "question with id {question_id} has been removed successfully!"
                        },200
              return jsonify(data)

           else:
                  
              data =    {
             "success":False,
             "message": "question with id {question_id} has been does not exist!"
                      }
              

          #  return jsonify(data)
   

         except Exception as e: 
           print(e)
           abort(404)
       
           
           

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/question',  methods = ['POST'])
    def handle_question_creation():
        try:
         request_data = request.get_json()
         question = request_data['question']
         answer = request_data['answer']
         category = request_data['category']
         difficulty = request_data['difficulty']

         quest = Question(
            question = question,
            answer = answer,
            category = category,
            difficulty = difficulty
        )
         db.session.add(quest)
         db.session.commit()
         return {
            "success":True,
            "message":'question has been created successfully!',
                      },200
        
        except Exception  as e:
          print('error occurred!', e)
          db.session.rollback()
          abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/api/questions/search',methods = ['POST'])
    def handle_questions_search():
          
          try:
            req = request.get_json()
            search = req['searchTerm']
            data = []      

            filteredList = Question.query.with_entities(Question.id,Question.question ,Question.answer, Question.category, Question.difficulty).filter(Question.question.like(f"%{search}%")).all()                                         
            for question in filteredList:
             data.append({
                 "id":question.id,
                 "question": question.question,
                 "answer": question.answer,
                 "category": question.category,
                 "difficulty": question.difficulty
             })
             
            return jsonify(data) 
          
          except Exception as error:
              print(error)
              return abort(404)
 

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
       
    @app.route('/api/categories/<int:category_id>/questions', methods = ['GET'])
    def handle_get_questions_by_category(category_id):
      try:

         questions = Question.query.filter(Question.category == str(category_id)).all()
         question = [question.format() for question in questions]
         
         if len(question) != 0:
          return jsonify({
              'success': True,
              'questions': question,
              'total_questions': len(question),
              'current_category': category_id
             }),200
         else:
          return jsonify({
               'success': False,
              'questions': [],
              'total_questions': len(question),
              'current_category': category_id,
              'message': 'no questions found with the specified category id found!',
             })
         
      except Exception as err:
          print(err)
          return abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/quizzes', methods = ['POST'])
    def handle_create_quiz():
        
        try:
           
          req = request.get_json()
          previous_questions = req['previous_questions']
          quizz_category = req['quiz_category']
          # print(quizz_category,'sdsd')


          if quizz_category['id'] == 0:
                questions = Question.query.filter(
                Question.id.not_in(previous_questions)).all()
                random_cquestion = random.choice(questions).format()
                return jsonify({
                   "success": True,
                   "question": random_cquestion
                               })
    

          else:
            questions_list = Question.query.filter(
                Question.category == quizz_category['id'],
                Question.id.not_in(previous_questions)).all()
      
      
            if len(questions_list) == 0:
                   return jsonify({
                "success": True,
                "questions": None
                })

            random_cquestion = random.choice(questions_list).format()

            return jsonify({
            "success": True,
            "question": random_cquestion
        })
    
        except Exception as error:
           print(error)
           return abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
       return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


    @app.errorhandler(422)
    def UnprocessableContent(error):
       return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Content'
    }), 422

    return app


