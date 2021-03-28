
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

Assistant = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ0ZHRvSUcwTVhVZW5aeW1YNmFOQSJ9.eyJpc3MiOiJodHRwczovL21lc2hhcmktZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MGNhNDUyY2RkM2UwMDY5YzYxZmNiIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MTY5NTY3NTMsImV4cCI6MTYxNzA0MzE1MywiYXpwIjoiQjlQaWJrd3JGSHJ5WU9wVEFkcnZCTWlqcjZmekJyOXAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.kIJsTRlnDmNt4-7vC8Op4KA9UxpGZVW-SGBNDC0fRW7dDdRhDDw6_6rwXqoEvPs75m814aIcWzyKi5j3WqCz-U_vO3Xgrft5D-xfYqKMQhs17fw8VjmtFH-GhwREswM0pBLc6AMAv7uafc-VEx0GhAgL44b-aEmDpi6lYcv2tXsy8EfUrmBpNJhrNCCPkV78HWA37FwTFuVjyGUsiMBNALAjsS9GZ1anFNxz3wGKqvj8DooUPixoByOIzBXq_DblG8fWkYyeCCEVuGNwA-haSuGs9z2BpIS6JVmaD9w560_llBPFbN7JgmWNYnIPMlvS0JIop8xhk6DQkasv2NkRZA'
}

Director = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ0ZHRvSUcwTVhVZW5aeW1YNmFOQSJ9.eyJpc3MiOiJodHRwczovL21lc2hhcmktZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MGNiMGYyY2RkM2UwMDY5YzYxZmRkIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MTY5NTY5OTMsImV4cCI6MTYxNzA0MzM5MywiYXpwIjoiQjlQaWJrd3JGSHJ5WU9wVEFkcnZCTWlqcjZmekJyOXAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIl19.KeIyTAc1K4RtE2YcoSye5t-0I71wUP4WLuvYgrw7-79zv9CwzkftfxcisvCPyOymbgeJ5UL6TD-EnCOewf2rf2pE8M83WLrXfl0j21U2TCzlZaaoy1Do6d6gX7GPkiEe9a7d1Tdvno4i3n2fZOqaIkkGoJFwj1r3Ptl7oRG2EzrEsWi_caQLfWj1fSNmoQNkNNsCSxVaT25kdtxfAsHKvSI_z-Jc1l93PbgdHLGIBNei1j0BLhw03rdXgEB7bGFB4ehV0q7Hp_AqSscO9uR3bJn32ekJzcrzJMf4McGPJCPu8IZpWt1TCbA_-jx4dhNO9HI-vFlmN8ztv4q7IGMDOA'
}

Executive = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ0ZHRvSUcwTVhVZW5aeW1YNmFOQSJ9.eyJpc3MiOiJodHRwczovL21lc2hhcmktZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA2MGNiYWM0OWQxODkwMDcyMWNiYzNiIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MTY5NTY4NjcsImV4cCI6MTYxNzA0MzI2NywiYXpwIjoiQjlQaWJrd3JGSHJ5WU9wVEFkcnZCTWlqcjZmekJyOXAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BTqZF2V_pfblkY1W9T-kc50YVhNFtOrpIqf3xkLJN7vOd1jFCvB-0aeKb-ZvCesxZhWH-rlliBtb4IXGEAb4alBNERyPsGgEeZqwNN0ALXXo36dUuHOTif-7ZQ_-0ERcx4Umv85c86FYDKgIpiaSej8_PA4ogael6GykV5y2D8i_JxdnWj9uvu2Zk7R7M7hSsUtpOnuQKhHyCPfjAnXSWxKoI1QbZ9-yeo376UTR44RfSkou6M4A0uLp-HZzNLWnSgsuk2pt0DZ-R8Y8EqHpOfJtYn1GvRLXfu_4rciQz_-kPoBO9EgzTV_0fescxZr2QQ5TMO8TJp1nlJGq_7RFwA'
}


class CapstonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app_test_client
        self.database_name = 'agencydb'
        db_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        self.database_path = db_path
        setup_db(self.app, self.database_path)
        #self.db.create_all()

    def tearDown(self):
        pass

#Get

    def test_get_actor(self):
        res = self.client().get('/actor', headers=Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['actor'], list)

    def test_get_movie(self):
        res = self.client().get('/movie', headers=Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['movie'], list)

    def test_get_actor_faild(self):
        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_movie_faild(self):
        res = self.client().get('/movie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

#Post

    def test_post_actor(self):
        res = self.client().post('/actor', header=Director, json={
            "name": "Mesho",
            "age": "99",
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_id'], 1)

    def test_post_movie(self):
        res = self.client().post('/movie', headers=Executive, json{
            "title": "GoodTimes",
            "release_date": "01/01/2001"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['create_id'], 1)

    def test_actor_post_failed(self):
        res = self.client().post('/actor', json={
            "name": "Memo",
            "age": "22",
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_movie_post_failed(self):
        res = self.client().post('/movie', json={
            "title": "BadTimes",
            "release_date": "10/04/2017"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


# Patch

    def test_patch_actor(self):
        res = self.client().patch('/actor/1', headers=Director, json={
            "name" = "Malak",
        })
        data = json.assertEqual(res.status_code, 200)

    def test_patch_movie(self):
        res = self.client().patch('/movie/1', headers=Executive, json={
            "title": "Timess",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_patch_actor_failed(self):
        res = self.client().patch('/actor/1', json={
            "name": "MeshMesh",
            "age": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_patch_movie_failed(self):
        res = self.client().patch('/movie/1', json={
            "title": "Lool",
            "release_date": "05/27/1994"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

# Delete

    def test_delete_actor(self):
        res = self.client().delete('/actor/1', headers=Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete_id'], 1)

    def test_delete_movie(self):
        res = self.client().delete('/movie/1', headers=Executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete_id'], 1)

    def test_delete_actor_failed(self):
        res = self.client().delete('/actor/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_movie_failed(self):
        res = self.client().delete('/movie/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()




    


