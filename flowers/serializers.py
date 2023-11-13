import hashlib
from django.core.files.temp import NamedTemporaryFile
from rest_framework import serializers
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
import numpy as np

from flowers.models import Image

SIZE = 128

FLOWERS_DICT = {
    'daisy': 'Margarita',
    'dandelion': 'Diente de león',
    'rose': 'Rosa',
    'sunflower': 'Girasol',
    'tulip': 'Tulipán',
}

class ImagePredictionSerializer(serializers.ModelSerializer):

    def generate_checksum(self, image):
        checksum = hashlib.md5(image.read()).hexdigest()
        return checksum
    
    def make_encoder(self):
        label_encoder = LabelEncoder()
        label_arr = np.array(['daisy', 'dandelion', 'rose', 'sunflower', 'tulip'])
        label_encoder.fit_transform(label_arr)
        return label_encoder
    
    def predict_image(self, image):
        loaded_model = load_model('trained_model.h5')
        new_image = load_img(image, target_size=(SIZE, SIZE))
        new_image_arr = img_to_array(new_image)
        new_image_arr = new_image_arr / 255.0
        new_image_arr = new_image_arr.reshape(1, SIZE, SIZE, 3)
        predictions = loaded_model.predict(new_image_arr)
        predicted_class = np.argmax(predictions)
        label_encoder = self.make_encoder()
        decoded_label = label_encoder.inverse_transform([predicted_class])[0]
        return FLOWERS_DICT.get(decoded_label, 'No reconocida'), predictions[0][predicted_class]

    def create(self, validated_data):
        image = validated_data['image']
        checksum = self.generate_checksum(image)
        saved_obj = Image.objects.filter(checksum=checksum).first()
        if saved_obj and saved_obj.prediction:
            print(f'Fetched from database: {saved_obj.checksum}')
            return {
                'image': saved_obj.image.url,
                'prediction': saved_obj.prediction,
                'accuracy': saved_obj.accuracy,
            }
        image_object = Image.objects.create(image=image, checksum=checksum)
        prediction, accuracy = self.predict_image(f'.{image_object.image.url}')
        image_object.prediction = prediction
        image_object.accuracy = round(accuracy * 100, 2)
        image_object.save()
        return {
            'image': image_object.image.url,
            'prediction': prediction,
            'accuracy': image_object.accuracy,
        }

    class Meta:
        model = Image
        fields = ('image',)