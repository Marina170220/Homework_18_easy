from flask import request
from flask_restx import Resource, Namespace

from app.models import MovieSchema, Movie
from app.setup_db import db


movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        dir_id = request.args.get('director_id')
        gen_id = request.args.get('genre_id')
        year = request.args.get('year')
        if dir_id:
            movies = Movie.query.filter(Movie.director_id == dir_id).all()
        elif gen_id:
            movies = Movie.query.filter(Movie.genre_id == gen_id).all()
        elif year:
            movies = Movie.query.filter(Movie.year == year).all()
        else:
            movies = Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200
        return "", 404

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
            return "", 201


@movie_ns.route('/<int:mov_id>')
class MovieView(Resource):
    def get(self, mov_id: int):

        try:
            movie = Movie.query.get(mov_id)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

    def put(self, mov_id: int):
        movie = Movie.query.get(mov_id)
        if movie:
            req_json = request.json
            movie.title = req_json.get('title')
            movie.description = req_json.get('description')
            movie.trailer = req_json.get('trailer')
            movie.year = req_json.get('year')
            movie.rating = req_json.get('rating')
            movie.genre_id = req_json.get('genre_id')
            movie.director_id = req_json.get('director_id')
            db.session.add(movie)
            db.session.commit()
            return "", 200
        return "", 404

    def delete(self, mov_id: int):
        movie = Movie.query.get(mov_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return "", 204
        return "", 404

