from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import base64
import io

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyBkQSeElRxt2jD98uc21JAxlKkiQkUNcOc")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize')
def recognize():
    return render_template('recognize.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data_url = request.json.get('image')
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_data))

    prompt = """
Analyze this food product and provide:
1. Age group suitability
2. Common additives/preservatives
3. Potential side effects (10 words max)
4. Key nutrients (5 words max)
5. Brief summary (2-3 lines)
Note: This is a general analysis based on the image.
"""

    response = model.generate_content([prompt, image])
    return jsonify({'result': response.text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)