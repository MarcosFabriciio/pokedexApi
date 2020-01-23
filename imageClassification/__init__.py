from tensorflow.keras.models import load_model
from tensorflow import cast
from tensorflow import float32
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import json


class ImageClassifier:

    def __init__(self):

        self.base64String = None
        self.imgSize = 300
        self.pokemonName = None
        self.dictJson = None
        self.model = None

    def predict(self, base64String):

        if self.model is None and self.dictJson is None:
            self.model = self.getModel()
            self.dictJson = self.loadDictFromJson()

        self.base64String = base64String
        image = self.base64ToImage()

        self.predictImg(image, self.model)

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
            return load_model("imageClassification/assets/secondeModel.h5")

        except Exception as e:
            raise e

    def loadDictFromJson(self):
        try:
            with open("imageClassification/assets/pokemonList.json") as jsonFile:
                names = json.load(jsonFile)
            jsonFile.close()

            return dict(names)

        except Exception as e:
            raise e

    def predictImg(self, image, model):
        try:
            pokemonDictNames = self.dictJson
            npImage = cast(np.array(image).reshape(-1, IMG_SIZE_X, IMG_SIZE_Y, 1), float32)
            pokemonClass = str(model.predict_classes(npImage)[0])
            self.pokemonName = pokemonDictNames[pokemonClass]

        except Exception as e:
            raise e
