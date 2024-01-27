# from flask_cors import CORS, cross_origin
# from flask import Flask, flash, redirect, request, session, url_for, jsonify

# load_dotenv()
# app = Flask(__name__)
# CORS(app)



import requests

# Your Imgur client ID
client_id = '8ddacd60b4380d0'

# Headers for authorization
headers = {'Authorization': 'Client-ID ' + client_id}

# Image to upload
image = {
    'image': open('testing_image.jpeg', 'rb').read()
}

# POST request to Imgur API
response = requests.post('https://api.imgur.com/3/upload', headers=headers, files=image)

# Extracting the URL of the uploaded image
url = response.json()['data']['link']

print(url)
