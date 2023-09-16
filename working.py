import requests
import json
import os

import spacy


nlp = spacy.load("en_core_web_sm")

# Text to be analyzed
text = '''It's a sunny day , children are playing football and cat and dogs are watching them.'''

# text='''Communication, both spoken and written, is always addressed to an audience, a set of listeners or readers you are intending to convey information to or have some effect upon. Public speaking differs from written communication in that the audience is present, gathered for some occasion. That occasion has norms and expectations that a speaker must recognize. Finally, a public speaker has some purpose, something they are trying to accomplish or set in motion. Good public speaking always accounts for these three components.'''
# text='''He lifted the bottle to his lips and took a sip of the drink. He had tasted this before, but he couldn't quite remember the time and place it had happened. He desperately searched his mind trying to locate and remember where he had tasted this when the bicycle ran over his foot.'''
# text='''The sun is shining brightly in the clear blue sky. Birds are chirping, and the flowers in the garden are in full bloom. It's a beautiful day to go for a walk and enjoy the beauty of nature.'''


doc = nlp(text)


keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]

print(keywords)
print("Keywords:")
print(keywords)

# Replace 'YOUR_ACCESS_KEY' with your actual Unsplash access key
access_key = 'yqvAk-_EXJQAAPXYyysMoqkyYy9bRsnsRc_rHrKTs1Y'

def fetch_and_download_images(keywords, per_page=1, total_pages=1, download_folder="downloads"):
    # Create a folder for downloaded images if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)
    image_info = []

    j=1
    for keyword in keywords:
        for page in range(1, total_pages + 1):
            url = f'https://api.unsplash.com/search/photos?query={keyword}&per_page={per_page}&page={page}&client_id={access_key}'

            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                for i, photo in enumerate(data['results']):
                    image_url = photo['urls']['regular']
                    image_extension = image_url.split('.')[-1]
                    image_filename = f"{j}.png"
                    print(j)
                    j=j+1
                    image_path = os.path.join(download_folder, image_filename)

                    # Download and save the image
                    with open(image_path, 'wb') as image_file:
                        image_file.write(requests.get(image_url).content)

                    # Store image information for HTML page
                    image_info.append({'url': image_url, 'filename': image_filename})
            else:
                print(f"Failed to fetch images for keyword '{keyword}' on page {page}")

    return image_info

# List of keywords for which you want to fetch images
# keyword_list = ["countryside", "city"]

# Number of images per keyword
images_per_keyword = 1

# Total pages to fetch (adjust based on your needs)
total_pages = 1

# Folder to save downloaded images
download_folder = "downloads"

fetched_image_info = fetch_and_download_images(keywords, per_page=images_per_keyword, total_pages=total_pages, download_folder=download_folder)

# Create an HTML page to display the fetched images
with open("Dimage_gallery.html", "w") as html_file:
    html_file.write("<html>\n<head>\n<title>Image Gallery</title>\n</head>\n<body>\n")
    
    for i, image_info in enumerate(fetched_image_info):
        html_file.write(f"<img src='{download_folder}/{image_info['filename']}' alt='Image {i + 1}' />\n")
    
    html_file.write("</body>\n</html>")

print("Images fetched, downloaded, and displayed on the HTML page.")


from moviepy.editor import ImageSequenceClip

import cv2

# Path to the directory containing your images
image_folder = 'downloads'

# Output video file name
video_name = 'output_video.mp4'

# Get a list of image files in the specified directory
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

# Sort the image filenames in the correct order
images.sort(key=lambda x: int(x.split('.')[0]))
print(images)

# Load the first image to get its dimensions
first_image = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = first_image.shape

# Create a list of resized and converted-to-RGB images with the same dimensions
resized_images = [cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(image_folder, image)), (width, height)), cv2.COLOR_BGR2RGB) for image in images]

clip = ImageSequenceClip(resized_images, fps=1)
clip.write_videofile(video_name, codec='libx264')

from googletrans import Translator
from gtts import gTTS
from IPython.display import Audio

# English text input by the user
english_text = text

# List of supported Indian languages and their language codes
indian_languages = {
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ur": "Urdu",
    "ml": "Malayalam",
    "or": "Oriya",
    "as": "Assamese"
}

# Let the user choose the target language
print("Select a target language:")
for code, lang in indian_languages.items():
    print(f"{code}: {lang}")

target_language = input("Enter the language code: ")

# Check if the selected language is supported
if target_language not in indian_languages:
    print("Selected language is not supported.")
else:
    # Initialize the Translator object
    translator = Translator()

    # Translate English text to the chosen Indian language
    translated_text = translator.translate(english_text, src='en', dest=target_language).text

    # Display the translated text on the screen
    print(f"Translation to {indian_languages[target_language]}:")
    print(translated_text)

    # Convert the translated text to audio in the same language
    tts = gTTS(translated_text, lang=target_language)
    audio_file = f"output.mp3"
    tts.save(audio_file)

    # Play the audio and download it
    print(f"Playing and downloading {indian_languages[target_language]} audio...")


from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

title = input("Enter a title: ")

video_clip = VideoFileClip("output_video.mp4")
audio_clip = AudioFileClip("output.mp3")

final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile(title + ".mp4")	
