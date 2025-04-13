from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = load_model('model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the image file as a BytesIO stream
        image_bytes = file.read()
        image = load_img(io.BytesIO(image_bytes), target_size=(225, 225))  # Use io.BytesIO

        # Preprocess the image
        x = img_to_array(image)
        x = x.astype('float32') / 255.0
        x = np.expand_dims(x, axis=0)

        # Make predictions
        predictions = model.predict(x)
        predicted_class = int(np.argmax(predictions, axis=1)[0])

        return jsonify({'predicted_class': predicted_class})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)