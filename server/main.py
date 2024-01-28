from flask_cors import CORS, cross_origin
from flask import Flask, flash, redirect, request, session, url_for, jsonify
from cohere_nlp import choose_songs, embed_music_and_captions, choose_dances, reply, classify_user_prompt


app = Flask(__name__)
CORS(app)

@app.route('/entry/', methods=['POST'])
def entry():
    prompt = request.get_json()['prompt']
    sentiment = classify_user_prompt(prompt)
    songs = choose_songs(prompt, sentiment)
    return jsonify(
        {'songs': songs}
    )

@app.route('/dance/', methods=['POST'])
def dance():
    song = request.get_json()['song']
    dances = choose_dances(song)
    return jsonify(
        {'dance': dances}
    )


@app.route('/images/', methods=['POST'])
def images():
    music = request.get_json()['music']
    image_urls_filtered = embed_music_and_captions(music) 
    return jsonify(
        {'images': image_urls_filtered}
    )



    
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)