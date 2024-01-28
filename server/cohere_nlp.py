import cohere
import os
import numpy as np 
import autofaiss
from image_captioning import generate_caption
from image_storing import get_image_url
from cohere.responses.classify import Example

api_key = os.environ.get("COHERE_API_KEY")
co = cohere.Client(api_key)

EXAMPLES = [
    Example("I want uplifting 2000s music!", "Energizing"),
    Example("I want to hear some iconic 80s pop songs.", "Energizing"),
    Example("Can you suggest mellow and slow songs?", "Soothing"),
    Example("Looking for melancholy disco tracks.", "Soothing")
]




SONGS = [
    # 1980s Songs
    {"title": "Don't Stop Believin'", "snippet": "Uplifting, journey-themed rock anthem."},
    {"title": "Sweet Child O' Mine", "snippet": "Iconic rock with memorable guitar riffs."},
    {"title": "Beat It", "snippet": "Fusion of rock and pop with a strong beat."},
    {"title": "Girls Just Want to Have Fun", "snippet": "Lively and upbeat pop anthem."},
    {"title": "Every Breath You Take", "snippet": "Soft rock with a haunting melody."},

    # 1990s Songs
    {"title": "Smells Like Teen Spirit", "snippet": "Grunge anthem with rebellious energy."},
    {"title": "Wonderwall", "snippet": "Iconic Britpop with a sing-along chorus."},
    {"title": "Creep", "snippet": "Alternative rock with introspective lyrics."},
    {"title": "U Can't Touch This", "snippet": "Catchy hip-hop with unforgettable hooks."},
    {"title": "Wannabe", "snippet": "Upbeat pop, symbolizing girl power."},
    {"title": "Enter Sandman", "snippet": "Hard rock with dark, intense energy."},
    {"title": "No Scrubs", "snippet": "R&B with empowering, independent themes."},
    {"title": "Torn", "snippet": "Emotional pop with a sense of longing."},
    {"title": "Killing Me Softly", "snippet": "Soulful and smooth R&B ballad."},
    {"title": "My Heart Will Go On", "snippet": "Dramatic, romantic ballad."},

    # 2000s Songs
    {"title": "Hey Ya!", "snippet": "High-energy, funky pop song."},
    {"title": "Crazy", "snippet": "Soulful and catchy pop tune."},
    {"title": "Hips Don't Lie", "snippet": "Latin-infused pop with danceable rhythm."},
    {"title": "Umbrella", "snippet": "R&B pop with a memorable chorus."},
    {"title": "Single Ladies", "snippet": "Upbeat pop with an empowering message."},
    {"title": "In da Club", "snippet": "Hip-hop track with a strong beat."},
    {"title": "Rolling in the Deep", "snippet": "Powerful vocal performance with deep emotion."},
    {"title": "I Gotta Feeling", "snippet": "Energetic pop perfect for parties."},
    {"title": "Poker Face", "snippet": "Electropop with catchy and dynamic beats."},
    {"title": "Viva la Vida", "snippet": "Orchestral pop with historic and artistic references."},
    {"title": "Toxic", "snippet": "Dance-pop with a seductive and catchy tune."},
    {"title": "Crazy in Love", "snippet": "R&B with strong vocals and a catchy beat."},
    {"title": "Bad Romance", "snippet": "Dark, dance-pop with unique sound."},
    {"title": "Mr. Brightside", "snippet": "Indie rock with enduring popularity."},
    {"title": "Lose Yourself", "snippet": "Motivational hip-hop with intense lyrics."},
    {"title": "Empire State of Mind", "snippet": "Hip-hop anthem with a soulful chorus."},
    {"title": "Fireflies", "snippet": "Electropop with dreamy and whimsical vibes."},
    {"title": "Bleeding Love", "snippet": "Soulful pop ballad about intense love."},
    {"title": "Rehab", "snippet": "Soul/jazz influenced track with catchy rhythms."},
    {"title": "Chasing Cars", "snippet": "Soft rock ballad with a touching melody."},

    # 2010s Songs
    {"title": "Shape of You", "snippet": "Catchy pop with an upbeat, danceable rhythm."},
    {"title": "Thinking Out Loud", "snippet": "Romantic ballad with soulful vocals."},
    {"title": "Despacito", "snippet": "Reggaeton-pop with a catchy, dance-inducing beat."},
    {"title": "Hello", "snippet": "Powerful ballad with emotive vocals."},
    {"title": "Uptown Funk", "snippet": "Funky and upbeat with retro vibes."},
    {"title": "Someone Like You", "snippet": "Emotional and soulful piano ballad."}
    ]


def embed_music_and_captions(music):
    # index 1 will be music, others wil be captions
    # captions will be a list of dictionaries, one per image
    k = 100
    image_paths = [f'image{i}.jpg' for i in range(1, 4)]
    image_urls = [get_image_url(image_path) for image_path in image_paths]
    captions = [generate_caption(image) for image in image_urls]

    combined_captions = [f'{caption_dict["text"]}\n{", ".join(caption_dict["tags"])}' for caption_dict in captions]
    combined_music_and_captions = [music] + combined_captions
    embeddings = np.array(co.embed(combined_music_and_captions).embeddings)

    index, stats = autofaiss.build_index(embeddings[1:])
    if len(image_urls) > k:
        dist, idx = index.search(np.array([embeddings[0]]), k=k)
        selected_captions = [captions[i] for i in idx[0]]
        results = co.rerank(query=f"Give the image captions that match {music}", documents=selected_captions, top_n=6, model="rerank-multilingual-v2.0")
        return [image_urls[hit.index] for hit in results]
    else:
        dist, idx = index.search(np.array([embeddings[0]]), k=6)
        return [image_urls[i] for i in idx[0]]

def choose_songs(prompt, sentiment):
    song_descriptions = [song['snippet'] for song in SONGS]
    classifications = co.classify(inputs=song_descriptions, examples=EXAMPLES)
    filtered_songs = [SONGS[i] for i in range(len(song_descriptions)) if classifications[i].prediction == sentiment]

    
    response = co.chat(
    model="command",
    message=f"Give me 5 comma separated songs and nothing else matching the chat history's format perfectly given this user's prompt:\n{prompt}",
    chat_history=[
        {"role": "User", "message": "I want uplifting 2000s music"},
        {"role": "Chatbot", "message": "'Hey Ya!', 'Crazy', 'I Gotta Feeling', 'Umbrella', 'Viva la Vida'"},
        {"role": "User", "message": "I want to hear some iconic 80s pop songs."},
        {"role": "Chatbot", "message": "'Billie Jean', 'Like a Virgin', 'When Doves Cry', 'Sweet Dreams', 'Every Breath You Take'"},
        {"role": "User", "message": "Can you suggest some classic country songs?"},
        {"role": "Chatbot", "message": "'Jolene', 'Ring of Fire', 'Crazy', 'Take Me Home, Country Roads', 'Stand By Your Man'"},
        {"role": "User", "message": "Looking for upbeat disco tracks."},
        {"role": "Chatbot", "message": "'Stayin' Alive', 'Le Freak', 'Dancing Queen', 'Super Freak', 'I Will Survive'"}
    ],
    documents=filtered_songs,
    temperature=0.0, 
    prompt_truncation="OFF", 
    stream=False,
    )

    cleaned = response.text.split(', ')
    if len(cleaned) != 5:
        return ['Hey Ya!', 'Crazy', 'I Gotta Feeling', 'Umbrella', 'Viva la Vida']
# print(choose_song('I feel like joyful 80s music'))


def reply(prompt, context):
    #context format {'song':, 'chosen_image_captions':, 'initial_prompt':}
    captions = '\n'.join([f'''Image{i+1} text:{captions[i]["text"]} Image{i} tags:{", ".join(captions[i]["tags"])}''' for i in range(len(captions))])
    response = co.chat(
    model="command",
    message=f"""Respond to the user's prompt {prompt} based on their initial prompt {context['initial_prompt']}, \
        the matched song {context['song']} and their past images which matched the song {captions}""",
    chat_history=[
        {"role": "User", "message": "I want uplifting 2000s music"},
        {"role": "Chatbot", "message": "'Hey Ya!', 'Crazy', 'I Gotta Feeling', 'Umbrella', 'Viva la Vida'"},
        {"role": "User", "message": "I want to hear some iconic 80s pop songs."},
        {"role": "Chatbot", "message": "'Billie Jean', 'Like a Virgin', 'When Doves Cry', 'Sweet Dreams', 'Every Breath You Take'"},
        {"role": "User", "message": "Can you suggest mellow country songs?"},
        {"role": "Chatbot", "message": "'Jolene', 'Ring of Fire', 'Crazy', 'Take Me Home, Country Roads', 'Stand By Your Man'"},
        {"role": "User", "message": "Looking for melancholy disco tracks."},
        {"role": "Chatbot", "message": "'Stayin' Alive', 'Le Freak', 'Dancing Queen', 'Super Freak', 'I Will Survive'"}
    ],
    temperature=0.0, 
    prompt_truncation="OFF", 
    stream=False,
)



def classify_user_prompt(prompt):
 

    response = co.classify(
        inputs=[prompt],
        examples=EXAMPLES,
    )
    return response[0].prediction








