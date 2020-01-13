from keras.models import load_model
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import json


class ImageClassifier:
    def __init__(self, base64String):
        self.base64String = base64String
        self.imgSize = 300
        self.pokemonDict = None
        self.pokemonName = None

    def predict(self):
        #Metodos para serem rodados apenas uma vez:
        model = self.getModel()
        self.loadDictFromJson()
        
        #Metodos que devem rodar para a classificação da imagem
        image = self.base64ToImage()
        self.predictImg(image, model)

    def base64ToImage(self):
        try:
            renderFromBase64 = Image.open(BytesIO(base64.decodebytes(bytes(self.base64String, 'utf-8'))))
            grayScale = renderFromBase64.convert("L")
            resizedGrayScale = grayScale.resize((self.imgSize, self.imgSize), Image.ANTIALIAS)

            return resizedGrayScale

        except Exception as e:
            raise e

    def getModel(self):
        try:
            model = load_model("assets/pokedex.h5")

            return model

        except Exception as e:
            raise e


    def loadDictFromJson(self):
        try:
            with open("assets/pokemonList.json") as jsonFile:
                names = json.load(jsonFile)
            jsonFile.close()

            self.pokemonDict = dict(names)

        except Exception as e:
            raise e

    def predictImg(self, image, model):
        try:
            npImage = np.array(image).reshape(-1, self.imgSize, self.imgSize, 1)
            pokemonClass = str(model.predict_classes(npImage)[0])
            pokemonDictNames = self.pokemonDict

            self.pokemonName = pokemonDictNames[pokemonClass]

        except Exception as e:
            raise e
