
from flask import jsonify
from flaskr import create_app
from models import setup_db, Question, Category
import os
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

        self.question = {"question": "Anansi Boys", "answer":'games',"category":"games" ,"difficulty": 5}
        

    def tearDown(self):
        pass

    
    def test_get_categories(self):
        res = self.client().get("/api/categories?page=200")
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(data["categories"])



    def test_get_paginated_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])




    def test_create_question(self):
        res = self.client().post("/api/question",json =self.question)
        data = res.get_json()
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
    


    def test_404_question_creation(self):
        res = self.client().post("/api/question", json='self.question')
        self.assertEqual(res.status_code, 404)


    def test_delete_question_(self):
        res = self.client().delete("/api/question/1")
        question = Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)


    def test_200_search_question(self):
        res = self.client().post("/api/questions/search", json = {"searchTerm":'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # self.assertTrue(data['question'])
        # self.assertTrue(data['answer'])

    def test_404_search_question(self):
        res = self.client().post("/api/questions/search", json = {"search":'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        


    def test_200_get_questions_based_on_category_id(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        # self.assertEqual(data['current_category'], category_id)



    # def test_404_get_questions_based_on_category_id(self):
    #         res = self.client().get('/api/categories/200/questions')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 404)
            # self.assertEqual(data['success'], False)
            # self.assertEqual(data['message'], 'Resource not found')

    def test_get_question_for_quiz_success(self):
        res = self.client().post("/api/quizzes", json={
            "previous_questions": [],
            "quiz_category": { "id": 1, "type": "travel"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

if __name__ == "__main__":
    unittest.main()