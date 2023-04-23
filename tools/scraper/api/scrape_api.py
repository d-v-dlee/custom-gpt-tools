import time
from flask import Flask, request, send_from_directory, jsonify
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory(os.path.join(app.root_path, '.well-known'), 'ai-plugin.json', mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory(os.path.join(app.root_path, '.well-known'), 'openapi.yaml', mimetype='text/yaml')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()

    # Validate input data
    if 'url' not in data:
        return jsonify({"error": "Missing URL parameter"}), 400

    url = data['url']

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    time.sleep(5)
    soup = BeautifulSoup(response.content, 'html.parser')
    scraped_data = soup.get_text()

    return jsonify({"scraped_data": scraped_data})

if __name__ == '__main__':
    app.run()
