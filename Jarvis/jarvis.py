import pyttsx3
from decouple import config
import speech_recognition as sr
from random import choice
from utils import opening_text
from datetime import datetime

# Assuming env_path is the path to your .env file
env_path = "C:\\Users\\shaya\\Downloads\\mediapipe-0.8.11\\mediapipe-0.8.11\\mediapipe\\tasks\\python\\Jarvis\\jarvis.env"

# Set the DOTENV_FILE attribute of the Config class
config.DOTENV_FILE = env_path

# Read the configuration from the .env file
USERNAME = config("USER", default="", cast=str)


env_path = "C:\\Users\\shaya\\Downloads\\mediapipe-0.8.11\\mediapipe-0.8.11\\mediapipe\\tasks\\python\\Jarvis\\jarvis.env"

# Set the DOTENV_FILE attribute of the Config class
config.DOTENV_FILE = env_path
BOTNAME = config("BOTNAME", default="", cast=str)



engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Used to speak whatever text is passed to it"""
    
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
        print("Good morning")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
        print("Good Afternoon")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
        print("Good Evening")
    speak(f"I am JARVIS. How may I assist you?")
    print("I am JARVIS. How may I assist you?")

def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if 'hello' or 'hi' or 'hello jarvis' or 'hi jarvis':
            speak("Hi, how can I help you?")
        elif not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
            print(f"You: {query}")
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night, take care!")
            else:
                speak('Have a good day!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query