from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)

# Load the OpenAI API key from an environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Set the OPENAI_API_KEY environment variable.")

@app.route('/')
def index():
    # Render your HTML page
    return render_template('index.html')

@app.route('/generate-image', methods=['POST', 'GET'])
def generate_image():
    # Validate the prompt
    prompt = request.form.get('prompt')
    if not prompt:
        return render_template('display_image.html', image_url='https://something', prompt="Error: No prompt provided")

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "model": "dall-e-3",
    }
    """    
    # Running tests cost-free
    image_url = 'https://something'
    return render_template('display_image.html', image_url=image_url, prompt=prompt)
    """
    try:
        response = requests.post('https://api.openai.com/v1/images/generations',
                                 headers=headers,
                                 data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            # Further processing of the image data could be done here
            image_url = data['data'][0]['url']
            return render_template('display_image.html', image_url=image_url, prompt=prompt)
        else:
            return f"Error: {response.status_code} - {response.text}", response.status_code
    except requests.RequestException as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)