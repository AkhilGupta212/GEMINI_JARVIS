import speech_recognition as sr
import webbrowser
import pyttsx3
import music_libra
import requests
import json

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def gemini(command):
    API_KEY = "API_KEY"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    data = {
        "contents": [
            {
                "parts": [
                    {"text": command}
                ]
            }
        ]
    }
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    if response.status_code == 200:
        result = response.json()
        print("Gemini says:\n")
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        print("Error:", response.status_code, response.text)

def processComand(command):
    print(f"Processing command: {command}")
    if command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        if len(command.split(" ")) > 2:
            for i in range(2, len(command.split(" "))):
                song += "_" + command.split(" ")[i]
        song.replace("_", " ")
        if song in music_libra.music:
            speak(f"Playing {song.replace('_', ' ')}")
        else:
            speak("Sorry, I don't have that song in my library.")
            return
        link = music_libra.music[song]
        webbrowser.open(link)
    elif command.lower() == "open youtube":
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif command.lower() == "open google":
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif command.lower() == "open stack overflow":
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif command.lower() == "open github":
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif command.lower() == "open facebook":
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif command.lower() == "open twitter":
        speak("Opening Twitter")
        webbrowser.open("https://twitter.com")
    else:
        output = gemini(command)
        speak(output)

if __name__ == "__main__":
    speak("Initializing JARVIS...")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for the JARVIS keyword...")
                audio = r.listen(source)
                print("Processing...")
            word = r.recognize_google(audio).lower()
            print(f"Command received: {word}")
            if "jarvis" in word:
                speak("Yes, how can I assist you?")
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    processComand(command)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
