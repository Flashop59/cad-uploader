from flask import Flask, request, jsonify
import trimesh
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['modelFile']
    if not file or not file.filename.endswith('.igs'):
        return jsonify({'error': 'Invalid file format. Only .igs files are accepted.'}), 400

    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    try:
        mesh = trimesh.load(file_path, file_type='igs')
        volume = mesh.volume / 1000  # Volume in cm³

        # Pricing logic: For example, ₹1.50 per cm³
        price = volume * 1.50

        return jsonify({'volume': volume, 'price': price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
