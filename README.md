# FSND_Capstone_Casting_Agency
Fullstack Nanodegree - Casting Agency

# Casting Agency
This a project for the Udacity Full Stacke Developer Nanodegree. The project shows a working API for the backend part of a Casting Agency.


Application hosted on Heroku 

https://calm-caverns-56785.herokuapp.com/

# Motivation

This project to show my learning journey during this nanodegree

1.  Database with  **postgres**  and  **sqlalchemy**  (`models.py`)
2.  API  with  **Flask**  (`app.py`)
3.  TDD  **Unittest**  (`test_app.py`)
4.  Authorization &  Authentification **Auth0**  (`auth.py`)
5.  Deployment on  **`Heroku`**

## Working with the application locally
Make sure you have [python 3](https://www.python.org/downloads/) or later installed

1. **Clone The Repo**
    ```bash
    git clone https://github.com/Meshari27/FSND_Capstone.git
    ```
2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/bin/activate 
    ```
3. **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```
4. **Export Environment Variables**

    Refer to the `setup.sh` file and export the environment variables for the project.

5. **Create Local Database**:

    Create a local database and export the database URI as an environment variable with the key `DATABASE_URL`.

6. **Run Database Migrations**:
    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run


## Testing
To run the tests, run
```bash
dropdb agencydb
createdb agencydb
python test_app.py # if running locally
```

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `https://calm-caverns-56785.herokuapp.com/`
* Authentication: This application use Auth0 service


Users in this application are:

* Assistant : Can view actors and movies
    * Email: meshtestassistant@gmail.com
    * Password: Test123!
* Director : Can delete and add actor + Assistant permissions
    * Email: meshari-1994t@outlook.com
    * Password: Test123!
* Executive: Full Access
    * Email: meshari.talal994@outlook.com
    * Password: Test123!

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 404 – resource not found
* 422 – unprocessable

### Endpoints

#### GET /actors

* General: Return list of actors in Database
* Sample: `curl -L -X GET 'https://calm-caverns-56785.herokuapp.com/actors' \
-H 'Authorization: Bearer Assisant_Token'`<br>

        {
            "actors": [
                {
                    "age": 11,
                    "gender": "male",
                    "id": 3,
                    "name": "Meshari"
                }
            ],
            "success": true
        }

#### GET /movies

* General: Return list of movies in Database
* Sample: `curl -L -X GET 'https://calm-caverns-56785.herokuapp.com/movies' \
-H 'Authorization: Bearer Assisant_Token'`<br>

        {
            "movies": [],
            "success": true
        }

#### POST /actors

* General:
    * Create actor using JSON Request Body
    * Return ID of created actor
* Sample: `curl -X POST 'https://calm-caverns-56785.herokuapp.com/actors' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name":"Mesharii",
    "age":1000,
    "gender":"male"
}'`

        {
            "created_id": 4,
            "success": true
        }

#### POST /movies

* General:
    * Create movie using JSON Request Body
    * Return ID of created movie
* Sample: `curl -X POST 'https://calm-caverns-56785.herokuapp.com/movies' \
-H 'Authorization: Bearer Executive_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"BadTimes",
    "release_date" : "03-03-2020"
}'`

        {
            "created_id": 2,
            "success": true
        }

#### PATCH /actors/<actor_id>

* General:
    * Modify actor given id in URL provided the information to update
* Sample: `curl -X PATCH 'https://calm-caverns-56785.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name" : "Meshari",
    "age" : 25
}'`

        {
            "actor": {
                "age": 25,
                "gender": "male",
                "id": 3,
                "name": "Meshari"
            },
            "success": true
        }
#### PATCH /movies/<movie_id>

* General:
    * Modify movie given id in URL provided the information to update
* Sample: `curl -X PATCH 'https://calm-caverns-56785.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"GoodTimes",
    "release_date":"10/19/2019"
}'`

#### DELETE /actors/<actor_id>

* General: Delete an actor given id in URL
* Sample: `curl -X DELETE 'https://calm-caverns-56785.herokuapp.com/actors/4' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 4,
            "success": true
        }

#### DELETE /movies/<movie_id>

* General: Delete movie given id in URL
* Sample: `curl -X DELETE 'https://calm-caverns-56785.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 2,
            "success": true
        }

# Postman user
in this repo there is collection file exported with latest postman version

you can use it to test all API Provided in here

PS: Update Tokens For Folders in the collection