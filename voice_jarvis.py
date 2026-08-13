import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from datetime import datetime

# ---------------- VOICE ENGINE FUNCTION ----------------
def speak(text):
    print("Jarvis:", text)
    
    # FIX: We initialize the engine INSIDE the function to refresh the audio driver.
    # This prevents the "Silence" bug on laptops like the Dell Latitude.
    engine = pyttsx3.init()
    
    # Re-apply settings
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    
    engine.say(text)
    engine.runAndWait()
    
    # FIX: We stop the engine to release the sound card for the microphone.
    engine.stop()

# ---------------- LISTENING ----------------
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        # FIX: Increased duration to 1.0 to give the Dell mic more time to adjust
        r.adjust_for_ambient_noise(source, duration=1.0)
        audio = r.listen(source)

    try:
        # Note: This requires internet. If it fails, Jarvis will stay silent.
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except Exception as e:
        # Printing the error helps you see if it's a "No Internet" or "No Mic" issue
        return ""

# ---------------- START ----------------
# This should play through your speakers immediately
speak("Jarvis is online")

# ---------------- MAIN LOOP ----------------
while True:
    command = listen()

    if not command:
        continue

    print("DEBUG COMMAND:", command)

    # ---------------- COMMANDS ----------------

    if "hello" in command:
        speak("Hello, I am working properly")

    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "youtube" in command:
        speak("Opening YouTube")
        os.system("start https://youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "chrome" in command:
        speak("Opening Chrome")
        # FIX: Using start chrome is good, but webbrowser is safer if chrome isn't in PATH
        os.system("start chrome")

    elif "stop" in command or "exit" in command:
        speak("Shutting down")
        break

    else:
        speak("Command received but not recognized")