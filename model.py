import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

class ImageClassifier:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        if self.model is None:
            self.model = MobileNetV2(weights='imagenet')
    
    def predict_image(self, image_path):
        self.load_model()
        
        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Make prediction
        preds = self.model.predict(x)
        decoded_preds = decode_predictions(preds, top=1)[0]
        
        # Get the class name and confidence
        class_name = decoded_preds[0][1].replace('_', ' ').title()
        confidence = float(decoded_preds[0][2]) * 100
        
        return class_name, confidence

# Create a global instance
classifier = ImageClassifier()

def predict_image(image_path):
    return class_name, confidence
