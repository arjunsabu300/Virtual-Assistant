import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests  # For weather information

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishME():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")
    
    speak("I am Jarvis. Please tell me how can I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query)
        return query.lower()
    except Exception as e:
        print("Say that again please....")
        return "none"

def get_weather():
    api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = "your_city"  # Replace with your city or use a user input
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    
    if data['cod'] != '404':
        weather_data = data['main']
        temperature = weather_data['temp'] - 273.15  # Convert from Kelvin to Celsius
        weather_desc = data['weather'][0]['description']
        speak(f"The temperature is {temperature:.2f} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found.")

if __name__ == "__main__":
    wishME()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for your query. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                speak("I couldn't find any information on that topic.")
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'weather' in query:
            get_weather()
        elif 'set reminder' in query:
            # Implement reminder functionality
            speak("Reminder functionality is not yet implemented.")
        elif 'joke' in query:
            # You can use an API to fetch jokes or hardcode some jokes
            speak("Why don't scientists trust atoms? Because they make up everything!")
        elif 'exit' in query:
            speak("Goodbye Boss!")
            break
