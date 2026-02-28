import os
import pyttsx3
from decouple import config, Config, RepositoryEnv
import speech_recognition as sr
from random import choice
from utils import opening_text
from datetime import datetime

# ── Load .env from the same directory as this file ───────────────────────────
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.env")
_config = Config(RepositoryEnv(_env_path))

USERNAME = _config("USER", default="", cast=str)
BOTNAME = _config("BOTNAME", default="JARVIS", cast=str)

# ── TTS engine ────────────────────────────────────────────────────────────────
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    """Speak the given text aloud."""
    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greet the user based on the current time."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


def take_user_input():
    """Listen for a voice command and return it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening…")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing…")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")

        q = query.lower()

        if 'exit' in q or 'stop' in q:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Good night, take care!")
            else:
                speak("Have a good day!")
            exit()

        if q in ('hello', 'hi', 'hello jarvis', 'hi jarvis'):
            speak("Hi, how can I help you?")
        else:
            speak(choice(opening_text))

    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Could you please say that again?")
        query = "None"
    except sr.RequestError:
        speak("I am having trouble connecting to the speech service. Please check your internet connection.")
        query = "None"
    except Exception:
        speak("Something went wrong. Please try again.")
        query = "None"

    return query
