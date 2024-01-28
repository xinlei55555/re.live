import os
import requests


TEST_PATH = 'testing_image.py'

def get_image_url(image_path):
    # Your Imgur client ID
    client_id = os.environ["IMGUR_API_KEY"]

    # Headers for authorization
    headers = {'Authorization': 'Client-ID ' + client_id}

    # Image to upload
    image = {
        'image': open(image_path, 'rb').read()
    }

    # POST request to Imgur API
    response = requests.post('https://api.imgur.com/3/upload', headers=headers, files=image)

    # Extracting the URL of the uploaded image
    url = response.json()['data']['link']

    return url
