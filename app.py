import os
import sys
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resource={r"/api/*": {"origins": "*"}})

    @app.route('/home')
    def index():
        return 'Boooooooooooooooooooooooooooooooo'



    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():
      try:
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        return jsonify({
          'success': True,
          'actors': actors
          })
      except:
        abort(404)


    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(self):
      try:
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        return jsonify({
          'success': True,
          'movies': movies
        })
      except:
        abort(422)



    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(self, id):
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor:
        actor.delete()
      else:
        abort(404)

      return jsonify({
        'success': True,
        'delete': id
      })
    
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(self, id):
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie:
        movie.delete()
      else:
        abort(404)

      return jsonify({
        'success': True,
        'delete': id
      })



    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(self):
      try:
        body = request.get_json()
        actor = Actor(
          name=body.get('name'),
          age=body.get('age'),
          gender=body.get('gender'),
        )
        actor.insert()

        return jsonify({
          'scueess': True,
          'actors': actor.format()
        }), 200
      except:
        print(sys.exc_info())
        abort(422)


      @app.route('/movies', methods=['POST'])
      @requires_auth('post:movies')
      def post_movie(self):
        try:
          body = request.get_json()
          movie = Movie(
            title=body.get('title'),
            release_date=body.get('release_date'),
          )

          movie.insert()

          return jsonify({
            'success': True,
            'actors': movie.format()
          }), 200

        except:
          print(sys.exc_info())
          abort(422)



      @app.route('/actors/<int:actor_id>', methods=['PATCH'])
      @requires_auth('patch:actors')
      def edit_actor(self, actor_id):
        try:
          body = request.get_json()
          actor = Actor.query.get(actor_id)
          if not actor:
            abort(404)
          actor.name = body.get('name')
          actor.age = body.get('age')
          actor.gender = body.get('gender')

          actor.update()

        except:
          print(sys.exc_info())
          abort(422)

        return jsonify({
          'success': True,
          'actors': [actor.format()]
        }), 200


      @app.route('/movies/<int:movie_id>', methods=['PATCH'])
      @requires_auth('patch:movies')
      def edit_movie(self, movie_id):
        try:
          body = request.get_json()
          movie = Movie.query.get(movie_id)
          if not movie:
            abort(404)
          movie.title = body.get('title')
          movie.release_date = body.get('release_date')

          movie.update()

        except:
          print(sys.exc_info())
          abort(422)

        return jsonify({
          'success': True,
          'movies': [movie.forma()]
        }), 200


  
    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
      }), 422


    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404


    return app



app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)