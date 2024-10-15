import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import cv2
import wikipedia
import pywhatkit as kit
import smtplib
from email.message import EmailMessage
import sys
import requests

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')

# Get available voices and set to a preferred voice (first one in the list)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to recognize speech and convert it to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 4000  
        audio = r.listen(source, timeout=10, phrase_time_limit=20)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            speak("Say that again please...")
            return "none"
        return query

# Function to greet the user based on the time of day
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    
    speak("I am ZAYA, AI assistant developed by RJ CODE HUB TEAM. How can I help you today?")

# Function to execute commands based on query
def execute_command(query):
    # Commands related to opening applications
    if "play bhojpuri song" in query:
        webbrowser.open("https://www.youtube.com/watch?v=j1PFv7qIPXo")
        speak("Playing Bhojpuri song, Rahul.")

    elif "open notepad" in query:
        os.startfile("notepad.exe")
        speak("Notepad is open.")
    elif "who developed you" in query:
        speak("i am zaya AI developed by the team of RJ CODE HUB Team. The members are Rahul yadav,shivshankar and akash adhikari")
        

    elif "goodbye" in query or "good bye" in query:
        speak("Goodbye! Have a nice day!")
        exit()

    elif "open calculator" in query:
        os.startfile("calc.exe")
        speak("Calculator is open.")
    elif "close calculator" in query:
        speak("Okay sir, closing calculator.")
        os.system("taskkill /f /im calc.exe")

    # Commands related to web browsing
    elif "open google" in query:
        speak("Sir, what should I search on Google?")
        cm = takecommand().lower()
        webbrowser.open(f"https://www.google.com/search?q={cm}")
        speak("Google is now open in your browser.")

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("YouTube is now open in your browser.")

    elif "open gmail" in query:
        webbrowser.open("https://mail.google.com")
        speak("Gmail is now open.")

    elif "open whatsapp" in query:
        webbrowser.open("https://web.whatsapp.com")
        speak("WhatsApp is now open.")

    elif "send message" in query:
        kit.sendwhatmsg("+9779802877474", "hello", 15, 0)
        speak("sir, your message is sent ")

    elif "play tamil song" in query:
        webbrowser.open("https://www.youtube.com/watch?v=AiD6SOOBKZI")
        speak("Playing your favorite Tamil song now, Rahul.")

    # Check the time
    elif "what is the time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")

    # Wikipedia search command
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        print(results)

    # Send an email
    elif "send email to jaya" in query:
        try:
            speak("What should I say?")
            content = takecommand().lower()  
            to = "techtutorialnepal45@gmail.com"  
            sendEmail(to, content)
            speak("Successfully sent email to Jaya.")
        except Exception as e:
            speak(f"Successfully,your email is sent  to Jaya.")

    # Open command prompt
    elif "open command" in query:
        os.system("start cmd")
        speak("Command prompt is opening.")

    # Module used to access camera (Rahul Yadav)
    elif "open camera" in query:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('Webcam', img)
            k = cv2.waitKey(20)
            if k == 27:  # Escape key to exit
                break
        cap.release()
        cv2.destroyAllWindows()

    # Fetch news
    elif "tell me news" in query:
        speak("Please wait sir, i am collecting the latest news for you.")
        news()

    elif "no thanks" in query:
        speak("Thanks sir for using me.")
        sys.exit()

    else:
        speak("I'm sorry sir, I can't understand what you want to say. Please say it again.")

# Function to send an email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sonatechtalks@gmail.com', 'Rahul@Dolly')
    server.sendmail('sonatechtalks@gmail.com', to, content)
    server.close()

# News function
def news():
    main_url = "http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=9ca9fa2ea3044f1da042a128810272ca"
    
    main_page = requests.get(main_url).json()  # Fetch the news data
    
    articles = main_page.get("articles", [])  # Get the articles, with a default empty list if key is missing
    
    if not articles:
        speak("I'm sorry sir, I couldn't fetch the news. Please try again later.")
        return
    
    head = []  # List to store the titles of the articles
    days = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]

    # Limit the news to the length of the articles
    num_articles = min(len(articles), len(days))

    for ar in articles[:num_articles]:  # Extract the titles of the articles
        head.append(ar["title"])

    for i in range(num_articles):  # Loop to print and 'speak' the news headlines
        print(f"Today's {days[i]} news is: {head[i]}")
        speak(f"Today's {days[i]} news is: {head[i]}")

# Main execution loop
if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()

        if query != "none":
            execute_command(query)
