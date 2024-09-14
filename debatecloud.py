import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from collections import defaultdict
nltk.download('stopwords')
from nltk.corpus import stopwords

def load_transcript(file_path):
    with open(file_path, 'r') as file:
        transcript = file.read()
    return transcript

def parse_transcript(transcript):
    speakers = defaultdict(str)
    lines = transcript.splitlines()
    current_speaker = None
    
    for line in lines:
        if line.startswith("TRUMP:"):
            current_speaker = "TRUMP"
            line = line.replace("TRUMP:", "").strip()
        elif line.startswith("HARRIS:"):
            current_speaker = "HARRIS"
            line = line.replace("HARRIS:", "").strip()
        elif line.startswith("MUIR:") or line.startswith("DAVIS:"):
            current_speaker = None
            
        if current_speaker:
            speakers[current_speaker] += " " + line
    
    return speakers

def generate_wordcloud(text, filename, max_words=130, background_color='white', colormap='viridis', mask=None, min_font_size=24, random_state=None, font_path=None):
    stop_words = set(stopwords.words('english'))
    custom_stopwords = {'a', 'donald', 'trump', 'is', 'the', 'former', 'president', 'and', 'would', 'you', 'let', 'people', 'something', 'kamala','harris'}
    stop_words.update(custom_stopwords)
    text = text.lower()

    wordcloud = WordCloud(
        max_words=max_words,
        background_color=background_color,
        colormap=colormap,
        stopwords=stop_words,
        min_font_size=min_font_size,
        mask=mask,
        random_state=random_state,
        font_path=font_path
    ).generate(text)
    
    plt.figure(figsize=(8, 4), dpi=100, facecolor=background_color)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    
    # Save png with high resolution
    plt.savefig(filename, format='png', dpi=1000, facecolor=background_color,bbox_inches='tight')
    plt.close()

file_path = 'transcript.txt'
transcript = load_transcript(file_path)
speakers_text = parse_transcript(transcript)
wordcloud_settings = {
    "trump": {
        "max_words": 100,
        "background_color": "#949494",
        "colormap": "Reds",
        "mask": np.array(Image.open('elephant.png').convert('L')),
        "font_path": "Roboto/Roboto-Black.ttf"
    },
    "harris": {
        "max_words": 100,
        "background_color": "#949494",
        "colormap": "Blues",
        "mask": np.array(Image.open('donkey.png').convert('L')),
        "font_path": "Roboto/Roboto-Black.ttf"
    }
}

num_clouds = 1
for speaker, text in speakers_text.items():
    settings = wordcloud_settings.get(speaker.lower(), {})
    
    for random_state in range(num_clouds):
        filename = f"{speaker.lower()}_wordcloud_{random_state}.png"
        
        generate_wordcloud(
            text, 
            filename, 
            max_words=settings.get('max_words', 100),
            background_color=settings.get('background_color', 'white'),
            colormap=settings.get('colormap', 'copper'),
            mask=settings.get('mask', None),
            min_font_size=24,
            random_state=random_state,  # Varying random_state
            font_path=settings.get('font_path', None)
        )
        print(f"Word cloud saved for {speaker} with random_state={random_state} as {filename}")