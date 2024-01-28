import requests
import os

TEST_URL = "https://fastly.picsum.photos/id/0/5000/3333.jpg?hmac=_j6ghY5fCfSD6tvtcV74zXivkJSPIfR9B8w34XeQmvU"

def generate_caption(image_url):
    # Endpoint URL from the sample call
    endpoint = "https://computer-visiona-pi.cognitiveservices.azure.com/vision/v3.1/describe"

    # Your subscription key
    subscription_key = os.environ["CV_API_KEY"]


    # Headers and parameters for the API request
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/json'}
    params = {'maxCandidates': '1'}

    # Body of the request with the image URL
    body = {'url': image_url}

    # Making the POST request
    response = requests.post(endpoint, headers=headers, params=params, json=body)

    # Getting the response in JSON format
    result = response.json()

    return {
        'tags': result['description']['tags'],
        'text': result['description']['captions'][0]['text']
    }

  