
from flask import jsonify
from flaskr import create_app
from models import setup_db, Question, Category,db
import os
import random
import unittest
import json
from faker import Faker

class TriviaTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "0000", "localhost:5432", self.database_name

        )

        self.question = {"question": "what is your name", "answer":'mamoun',"category":"science" ,"difficulty": 5}
        self.questions = {"id":300,"question": "what is my name", "answer":'udacity',"category":"science" ,"difficulty": 5}
        # self.client().post("/api/question", json ={"id":75,"question": "what is my name", "answer":'udacity',"category":"science" ,"difficulty": 5})
        
        
    def tearDown(self):
        pass



    def test_success_get_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(data["categories"])

    def test_failure_get_categories(self):
        res = self.client().get("/api/categories/2")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)



    def test_success_get_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

    def test_failure_get_questions(self):
        res = self.client().get("/api/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)



    def test_200_create_question(self):
        res = self.client().post("/api/question",json =self.question)
        data = res.get_json()
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
    
    def test_404_create_question(self):
        res = self.client().post("/api/question", json='self.question')
        data = res.get_json()
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
   


    def test_success_delete_question(self):
        # res1 =self.client().post("/api/question",json =self.questions)
     insert= self.client().post("/api/question", json={
        "question": "question1",
        "answer": " answer1",
        "category": "category1",
        "difficulty": 1
    })
     self.assertEqual(insert.status_code, 200)

     Questions = Question.query.all()
     question = [questions.format() for questions in Questions]
     id = question[0]['id']
     delete_res = self.client().delete(f"/api/question/{id}")
     self.assertEqual(delete_res.status_code, 200) 


    def test_failure_delete_question(self):
        res = self.client().delete("/api/question/200")
        self.assertEqual(res.status_code, 404)



    def test_200_search_question(self):
        res = self.client().post("/api/questions/search", json = {"searchTerm":'what'})
        self.assertEqual(res.status_code, 200)

    def test_404_search_question(self):
        res = self.client().post("/api/questions/search", json = {"search":'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        


    def test_200_get_questions_based_on_category_id(self):
        res = self.client().get('/api/categories/2/questions')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_get_questions_based_on_category_id(self):
            res = self.client().get('/api/categories/bad/questions')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')



    def test_get_question_for_quiz_success(self):
        res = self.client().post("/api/quizzes", json={'previous_questions':[], 'quiz_category': {"type": 'click', "id": 0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_question_for_quiz_failure(self):
        res = self.client().post("/api/quizzes", json={'previous_questions':[], 'quiz_category':''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)



if __name__ == "__main__":
    unittest.main()