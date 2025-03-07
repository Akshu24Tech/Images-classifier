from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
from model import predict_image
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file uploaded')
        return render_template('index.html')
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return render_template('index.html')
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a PNG, JPG, or JPEG image.')
        return render_template('index.html')
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get prediction
        prediction, confidence = predict_image(filepath)
        
        return render_template('result.html',
                             filename=filename,
                             prediction=prediction,
                             confidence=confidence)
    except Exception as e:
        flash(f'Error processing image: {str(e)}')
        return render_template('index.html')

def init_app():
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create an empty .gitkeep file in uploads folder
    with open(os.path.join(app.config['UPLOAD_FOLDER'], '.gitkeep'), 'w') as f:
        pass

if __name__ == '__main__':
    init_app()
    app.run(debug=True)

