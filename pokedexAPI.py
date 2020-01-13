from imageClassification import ImageClassifier
from flask import Flask
from flask_restful import Api, Resource, reqparse
import base64

app = Flask(__name__)
api = Api(app)


class Classification(Resource):

    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('base64string', location='json')
        args = parser.parse_args()

        classifier = ImageClassifier(args.get("base64string"))
        classifier.predict()
        pokemonName = classifier.pokemonName

        if pokemonName is not None:
            return pokemonName, 200
        else:
            return "Não foi possivel classificar, verifique a imagem", 500

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(Classification, "/pokedex/classification")
if __name__ == "__main__":
    app.run(threaded=False)
