import cohere
import os
import numpy as np 
import autofaiss
from image_captioning import generate_caption
from image_storing import get_image_url

api_key = os.environ.get("COHERE_API_KEY")
co = cohere.Client(api_key)

songs = [
    {"title": "Alone", "snippet": "A powerful ballad with emotional depth."},
    {"title": "Chain Reaction", "snippet": "Upbeat, vibrant, and catchy pop tune."},
    {"title": "Relax", "snippet": "Energetic with provocative and electrifying vibes."},
    {"title": "The Look of Love", "snippet": "Synthpop with heartfelt and introspective tones."},
    {"title": "Here I Go Again", "snippet": "A mix of loneliness and determination."},
    # ... additional songs from the 90s, 2000s, and 2010s will follow in a similar format ...
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


def embed_music_and_captions(music, image_urls):
    # index 1 will be music, others wil be captions
    # captions will be a list of dictionaries, one per image

    captions = [generate_caption(image) for image in image_urls]

    combined_captions = [f'{caption_dict["text"]}\n{", ".join(caption_dict["tags"])}' for caption_dict in captions]
    combined_music_and_captions = [music] + combined_captions
    embeddings = np.array(co.embed(combined_music_and_captions).embeddings)

    index, stats = autofaiss.build_index(embeddings[1:])
    dist, idx = index.search(np.array([embeddings[0]]), k=2)
    return [image_urls[i] for i in idx[0]]


def choose_song(prompt):
    response = co.chat(
    model="command",
    message=f"Give me exactly and only 5 comma separated songs matching this user's prompt:\n{prompt}",
    documents=SONGS)
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=100,
        temperature=0.8,
        stop_sequences=["--"],
        return_likelihoods="NONE",
        truncate="START",
    )
    return response.generations[0].text
print(choose(song('I feel like joyful 80s music')))



