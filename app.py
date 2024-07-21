from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
IP_CHECK_URL = "https://api.ipify.org?format=json"

@app.route('/fetch', methods=['POST'])
def fetch():
    if request.method != 'POST':
        return jsonify({"error": "Only POST requests are allowed"}), 405

    try:
        # Check Worker's IP
        ip_response = requests.get(IP_CHECK_URL)
        ip_data = ip_response.json()
        worker_ip = ip_data['ip']

        # Get data from the request
        request_data = request.json

        # Check if API key is provided in the request
        if 'apiKey' not in request_data:
            return jsonify({"error": "API key is missing"}), 400

        # Prepare new request to Gemini API
        gemini_response = requests.post(
            f"{GEMINI_API_URL}?key={request_data['apiKey']}",
            json=request_data['content'],
            headers={'Content-Type': 'application/json'}
        )

        # Get response from Gemini API
        gemini_data = gemini_response.json()

        # Prepare response with Gemini data and Worker's IP
        response_data = {
            'geminiResponse': gemini_data,
            'workerIP': worker_ip
        }

        # Return response
        return jsonify(response_data), gemini_response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app on all network interfaces (0.0.0.0) and enable debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
