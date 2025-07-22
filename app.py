from flask import Flask, request, jsonify
from flask_cors import CORS
from detector.blink_utils import detect_blink_rate
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin support for Flutter Web


@app.route('/')
def hello():
    return 'Hello from Railway!'

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # Optional: 50MB upload limit

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_video():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video uploaded"}), 400
        
        file = request.files["video"]
        
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        os.remove(filepath)
        print(f"Video file deleted: {filepath}")
        blink_count, result_message = detect_blink_rate(filepath)
        return jsonify({
            "blinks": blink_count,
            "message": result_message
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
