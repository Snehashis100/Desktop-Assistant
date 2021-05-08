import pyttsx3
import datetime
import speech_recognition as sr
import os
import random
import wikipedia
import webbrowser as wb
import pywhatkit as wapp
import requests
import json

def Speak(st):
    """Here we are setting voice of our assistant why checking the different methods of pyttsx3 module"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Selecting the female voice
    engine.setProperty('rate', 175)  # Setting the rate to 175 words per minute
    engine.say(st)
    engine.runAndWait()


def Wish_me(user):
    '''Assistant will wish me according to the time'''
    now = datetime.datetime.now().hour
    if 0 <= now < 12:
        Speak(f"Good Morning {user}, I am Jini. How may I help you?")
    elif 12 <= now < 18:
        Speak(f"Good Afternoon {user}, I am Jini . How may I help you?")
    else:
        Speak(f"Good Evening {user},I am Jini . How may I help you?")


def Todays_news():
    url = 'http://newsapi.org/v2/top-headlines?country=in&apiKey=632d6bec70874cad843839749bbea144'
    retrieve = requests.get(url=url)
    text = retrieve.text
    news = json.loads(text)
    news = news['articles']
    Speak("Today's news are")
    for new in news:
        if None not in new:
            print(f"{new['description']}\n")
            Speak(new['description'])
    Speak("Thank you")


def Recognizing():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        # print(sr.Microphone.list_microphone_names())    #gives the list of input devices which can be used
        print("Listening...")
        r.energy_threshold = 250
        r.pause_threshold = 0.5
        audio = r.listen(mic)
    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        if query != 'Group' or query != 'group':
            print(f"You said: {query}")

    except Exception as e:
        print("Sorry, Please say that again")
        return "None"
    return query


def Msg_Recognition():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        Speak("What message you want to send?")
        r.energy_threshold = 250
        r.pause_threshold = 0.5
        print("Waiting for the message...")
        audio = r.listen(mic)
    try:
        print("Recognizing")
        msg = r.recognize_google(audio, language='en-in')
        print(f"You said: {msg}")
    except Exception as e:
        Speak("Sorry, Please say that again")
        return "None"
    return msg


def user_name_Recognition():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        Speak("To whom you want to send the message")
        r.energy_threshold = 250
        r.pause_threshold = 0.5
        print("Waiting for the name...")
        audio = r.listen(mic)
    try:
        print("Recognizing")
        user = r.recognize_google(audio, language='en-in')
        msg = Msg_Recognition()

    except Exception as e:
        Speak("Sorry, Please say that name again")
        return "None", "None"
    return user, msg


if __name__ == '__main__':
    wapp_contact_list = {'man': '+91**********', 'dada': '+91**********', 'baba': '+91**********'}
    user_name=input("Before starting your virtual assistant please give us your name:")
    Wish_me(user_name)
    while True:
        query = Recognizing().lower()
        if ('wikipedia' in query) or ('who is ' in query):
            Speak("Searching..")
            query = query.replace("wikipedia", "")
            query = query.replace("who is ", "")
            results = wikipedia.summary(query, sentences=3)
            print(f"Results: {results}")
            Speak(f"According to Wikipedia {results}")

        elif 'open google' in query:
            Speak("Google is opening please wait")
            wb.open_new_tab('https://www.google.com')

        elif 'search' in query and 'google' in query:
            query = query.replace('search', '')
            query = query.replace('in google', '')
            Speak("Searching")
            wapp.search(query)

        elif 'open youtube' in query:
            Speak("YouTube is opening please wait")
            wb.open_new_tab('https://www.youtube.com')

        elif ('search' in query and 'youtube' in query) or ('play' in query and 'youtube' in query):
            query = query.replace('search', '')
            query = query.replace('youtube', '')
            Speak("Playing")
            wapp.playonyt(query)

        elif 'open stack overflow' in query:
            Speak("Stackoverflow is opening please wait")
            wb.open_new_tab('https://www.stackoverflow.com')

        elif 'open facebook' in query:
            Speak("Facebook is opening please wait")
            wb.open_new_tab('https://www.facebook.com')

        elif 'website of my college' in query:
            Speak("Opening your college website")
            wb.open_new_tab('https://www.gnit.ac.in')

        elif 'play music' in query:
            path = 'D:\\Songs'
            Speak("Opening music player please wait")
            songs = os.listdir(path)
            song = random.choice(songs)
            os.startfile(path + f'\\{song}')

        elif 'play video songs' in query:
            path = 'D:\\Videos'
            Speak("Opening video player please wait")
            videos = os.listdir(path)
            video = random.choice(videos)
            os.startfile(path + f"\\{video}")
            # not opening pycharm

        elif 'open pycharm' in query:
            path = 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.3\\bin\\pycharm64.exe'
            Speak("Opening Pycharm please wait")
            os.startfile(path)

        elif 'the time' in query:
            now = datetime.datetime.now().hour
            if 0 <= now < 12:
                current = datetime.datetime.now().strftime("[%H:%M]am of %Y-%m-%d")
                Speak(current)
            else:
                current = datetime.datetime.now().strftime("[%H:%M]pm of %Y-%m-%d")
                Speak(current)

        elif 'open whatsapp' in query:
            user_name, msg_to_sent = user_name_Recognition()
            user_name = user_name.lower()
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute + 2
            if user_name in wapp_contact_list.keys():
                print("Sending....")
                wapp.sendwhatmsg(wapp_contact_list[user_name], msg_to_sent, hour, minute, wait_time=30)
                Speak("Your message has been sent successfully")

            elif user_name == 'group':
                Speak("To which group you want to send the message")
                group = Recognizing()
                print("Sending....")
                wapp.sendwhatmsg_to_group('*******************', msg_to_sent, hour, minute, wait_time=30)
                Speak("Your message has been sent to the group successfully")

            else:
                Speak("This person may not be present in your whatsapp contact list or you might have pronounced it incorrectly")

        elif 'the news' in query:
            Todays_news()

        else:
                  
            pass
