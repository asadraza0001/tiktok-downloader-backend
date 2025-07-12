from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "TikTok Downloader Backend is Running ✅"

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format')

    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    try:
        snaptik_api = 'https://snaptik.app/abc2.php'
        payload = {'url': url}
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.post(snaptik_api, data=payload, headers=headers)
        if response.status_code != 200 or 'https://cdn.snaptik' not in response.text:
            return jsonify({'success': False, 'message': 'Failed to fetch download link'}), 500

        start = response.text.find('https://cdn.snaptik')
        end = response.text.find('.mp4', start) + 4
        download_url = response.text[start:end]

        return jsonify({'success': True, 'downloadUrl': download_url})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
