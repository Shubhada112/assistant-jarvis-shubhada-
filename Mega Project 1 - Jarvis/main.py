import speech_recognition as sr
import webbrowser
import pyttsx3
from musicLibrary import music
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "6be590ef340944489e23079f5ea128b2"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    #need some chnages to work this 
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ", 1)[1]  # Extract song name
            link = music.get(song)
            if link:
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, {song} is not in your music library.")
        except IndexError:
            speak("Please specify a song to play.")
        except Exception as e:
            speak(f"An error occurred while trying to play music: {e}")

            
    #need some chnages to work this 
    elif "news" in c.lower():
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            data = response.json()
            if response.status_code != 200:
                speak("I couldn't fetch the news right now. Please try again later.")
                return
            articles = data.get('articles', [])
            if not articles:
                speak("No news articles found.")
            else:
                speak("Here are the top headlines:")
                for article in articles[:5]:
                    speak(article['title'])
        except Exception as e:
            speak(f"An error occurred while fetching news: {e}")

if __name__ == "__main__":
    speak("Initializing Shubhada...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word (say 'Shubhada')...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                word = recognizer.recognize_google(audio)
                if word.lower() == "shubhada":
                    speak("Yes, I'm listening.")
                    with sr.Microphone() as source:
                        print("Shubhada is active. Please give a command...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Recognized command: {command}")

                        processCommand(command)
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
