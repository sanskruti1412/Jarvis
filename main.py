import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pygame
from openai import OpenAI
from gtts import gTTS

# 🔹 Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# 🔹 Check if API keys are set correctly
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is missing! Set it in your environment variables.")
    exit(1)

if not NEWS_API_KEY:
    print("Warning: NEWS_API_KEY is missing. News functionality will not work.")

# 🔹 Initialize speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# 🔹 Music library for playing YouTube songs
musicLibrary = {
    "stealth": "https://www.youtube.com/watch?v=U47Tr9BB_wE",
    "march": "https://www.youtube.com/watch?v=Xqeq4b5u_Xw",
    "skyfall": "https://www.youtube.com/watch?v=DeumyOzKqgI",
    "wolf": "https://www.youtube.com/watch?v=ThCH0U6aJpU"
}

# 🔹 Function to convert text to speech
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# 🔹 Function to process AI responses
def aiProcess(command):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't process that request."

# 🔹 Function to process voice commands
def processCommand(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        if song in musicLibrary:
            webbrowser.open(musicLibrary[song])
    elif "news" in command:
        if NEWS_API_KEY:
            try:
                response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get("articles", [])[:5]:  # Read only 5 news headlines
                        speak(article['title'])
                else:
                    speak("Sorry, I couldn't fetch the news.")
            except Exception as e:
                print(f"Error fetching news: {e}")
                speak("Sorry, there was an issue retrieving the news.")
        else:
            speak("News API key is missing. Please set it up.")
    else:
        output = aiProcess(command)
        speak(output)

# 🔹 Main execution loop
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("Listening for wake word...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)

            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis is active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Speech Recognition service is unavailable.")
        except Exception as e:
            print(f"Error: {e}")
