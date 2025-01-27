import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user input via microphone and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None
    return query.lower()

def greet():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def perform_task(command):
    """Perform tasks based on user commands."""
    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad.exe")
    elif "weather" in command:
        speak("Please tell me the city name.")
        city = listen()
        if city:
            api_key = "your_openweathermap_api_key"  # Replace with your API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url).json()
            if response.get("main"):
                temp = response["main"]["temp"]
                description = response["weather"][0]["description"]
                speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
            else:
                speak("I couldn't fetch the weather details. Please try again.")
    else:
        speak("Sorry, I can't perform that task yet.")

# Main loop
if __name__ == "__main__":
    greet()
    speak("How can I assist you today?")
    while True:
        user_command = listen()
        if user_command:
            if "exit" in user_command or "quit" in user_command:
                speak("Goodbye! Have a great day!")
                break
            perform_task(user_command)
