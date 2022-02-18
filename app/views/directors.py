from flask_restx import Namespace, Resource
from app.models import DirectorSchema, Director

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        if directors:
            return directors_schema.dump(directors), 200
        return "", 404


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    def get(self, dir_id: int):
        try:
            director = Director.query.get(dir_id)
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404
