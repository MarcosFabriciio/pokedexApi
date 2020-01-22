from imageClassification import ImageClassifier
from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__)
api = Api(app)


class Classification(Resource):

    def __init__(self):
        self.classifier = ImageClassifier()

    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('base64string', location='json')
        args = parser.parse_args()

        self.classifier.predict(args.get("base64string"))
        pokemonName = self.classifier.pokemonName

        if pokemonName is not None:
            apiPath = "https://pokeapi.co/api/v2/pokemon/"
            response = requests.get(apiPath + pokemonName.lower())

            print(response)

            if response.status_code == 200:
                return response.json(), 200
            else:
                return "Couldn't get the Pokémon data please try again", 500
        else:
            return "Couldn't classify the Pokémon image", 500
    
    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(Classification, "/pokedex/classification")
if __name__ == "__main__":
    app.run(host='192.168.1.108', threaded=False)
