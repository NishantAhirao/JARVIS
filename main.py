import speech_recognition as sr
import webbrowser as wb
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "43b051e40381433c9a5034846efec749"

url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=43b051e40381433c9a5034846efec749"
response = requests.get(url)

# Check if the request was successful

def aiProcess(command):
    client = OpenAI(
        api_key="sk-proj-8cmg7phCvfTEDFQbzu0TT3BlbkFJoBySc83T8YjrnPN8wqMu",
    )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
        {"role": "user", "content": command}
    ]
    )
    return completion.choices[0].message.content

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
# Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running long enough to hear the music
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def processCommand(c):
    if "open google" in c.lower():
        wb.open("https://google.com")
    elif "open facebook" in c.lower():
        wb.open("https://facebook.com")
    elif "open youtube" in c.lower():
        wb.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        wb.open(link)
    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            articles = data.get('articles', [])
            for i, article in enumerate(articles, 1):
                headline = article.get('title', 'No title')
                speak(f"{i}. {headline}") 
    else:
        output = aiProcess(c)
        speak(output)





if __name__ == "__main__":
    speak("Initialising Jarvis")

    while True:
        r = sr.Recognizer()
        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
            word =  r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes Boss")
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
                    command =  r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))
            # print(f"Sphinx error; {e}")  
