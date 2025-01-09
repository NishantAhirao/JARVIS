# Importing necessary libraries
import speech_recognition as sr  # For speech recognition from audio input
import webbrowser as wb  # To open URLs in the default web browser
import pyttsx3  # For text-to-speech conversion
import musicLibrary  # A custom library for storing music links (assumed to be predefined)
import requests  # To make HTTP requests (used for fetching news data)
from openai import OpenAI  # For interacting with OpenAI's GPT-based services
from gtts import gTTS  # Google Text-to-Speech library for generating audio from text
import pygame  # For playing MP3 files
import os  # For file handling (deleting temporary audio files)

# Initialize the recognizer for speech recognition
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# API key for accessing NewsAPI for fetching top headlines
newsapi = "43b051e40381433c9a5034846efec749"

# URL for fetching top headlines from NewsAPI
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
response = requests.get(url)  # Send GET request to fetch news

# Define the function to process commands using OpenAI
def aiProcess(command):
    # Initialize the OpenAI client with the API key
    client = OpenAI(
        api_key="sk-proj-8cmg7phCvfTEDFQbzu0TT3BlbkFJoBySc83T8YjrnPN8wqMu",
    )
    # Request a response from OpenAI GPT model
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the GPT model
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},  # System prompt
            {"role": "user", "content": command}  # User's command
        ]
    )
    # Return the assistant's response
    return completion.choices[0].message.content

# Text-to-speech using pyttsx3
def speak_old(text):
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait for the speech to complete

# Text-to-speech using Google Text-to-Speech (gTTS) and Pygame
def speak(text):
    tts = gTTS(text)  # Convert text to audio
    tts.save('temp.mp3')  # Save the audio as a temporary MP3 file

    pygame.mixer.init()  # Initialize Pygame mixer for playing audio
    pygame.mixer.music.load("temp.mp3")  # Load the MP3 file
    pygame.mixer.music.play()  # Play the MP3 file

    # Keep the program running until the audio playback finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()  # Unload the MP3 file
    os.remove("temp.mp3")  # Delete the temporary MP3 file

# Process the user's command and execute appropriate actions
def processCommand(c):
    if "open google" in c.lower():
        wb.open("https://google.com")  # Open Google in the web browser
    elif "open facebook" in c.lower():
        wb.open("https://facebook.com")  # Open Facebook in the web browser
    elif "open youtube" in c.lower():
        wb.open("https://youtube.com")  # Open YouTube in the web browser
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]  # Extract the song name
        link = musicLibrary.music[song]  # Get the song link from the music library
        wb.open(link)  # Open the song link in the web browser
    elif "news" in c.lower():
        # Fetch news headlines from NewsAPI
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            articles = data.get('articles', [])  # Extract the list of articles
            for i, article in enumerate(articles, 1):
                headline = article.get('title', 'No title')  # Get the headline of each article
                speak(f"{i}. {headline}")  # Speak out the headline
    else:
        # Use OpenAI to process the command and get a response
        output = aiProcess(c)
        speak(output)  # Speak out the response

# Main function for initializing Jarvis and handling user interactions
if __name__ == "__main__":
    speak("Initializing Jarvis")  # Speak out the initialization message

    while True:
        r = sr.Recognizer()  # Create a new recognizer instance
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")  # Listen for a wake word (e.g., "Jarvis")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
            word = r.recognize_google(audio)  # Recognize speech using Google Speech Recognition
            if word.lower() == "jarvis":  # Check if the wake word is detected
                speak("Yes Boss")  # Respond to the wake word
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
                    command = r.recognize_google(audio)  # Recognize the user's command

                    processCommand(command)  # Process the recognized command

        except Exception as e:
            print("error; {0}".format(e))  # Handle exceptions and print the error message
