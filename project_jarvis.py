from win32com.client import Dispatch
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import smtplib
import random

def speck_fun(str):
    print(str)
    speak.Speak(str)

def welcome():
    h = datetime.datetime.now().hour
    if h>5 and h<12:
        speck_fun("good morning")
    elif h<15:
        speck_fun("good afternoon")
    else:
        speck_fun("good evening")

    speck_fun("I am alexa, What can I do for you?")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        speck_fun("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        speck_fun("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        speck_fun("Say that again please...")
        return "None"
    return query

def sendEmail(to, containt):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('hemalparmar2017@gmail.com', 'a7048274947')
    server.sendmail('hemalparmar2017@gmail.com', to, containt)
    server.close()


if __name__ == '__main__':
    speak = Dispatch("SAPI.SpVoice")
    email = {"Anil" : "2017anilrathod@gmail.com", "Hemal" : "hemalparmar1999@gmail.com", "Hiral" : "hiralparmar1996@gmail.com"}
    while True:
        query = takeCommand().lower()

        if "alexa exit" in query:
            exit()

        elif "alexa" in query:

            welcome()
            while True:
                query = takeCommand().lower()

                if "thank you" in query:
                    break

                elif "open google" in query:
                    webbrowser.open("google.com")

                elif "open youtube" in query:
                    webbrowser.open("youtube.com")

                elif 'wikipedia' in query:
                    speck_fun('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speck_fun("According to Wikipedia")
                    # print(results)
                    speck_fun(results)

                elif 'the time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speck_fun(f"Sir, the time is {strTime}")

                elif "file open" in query:
                    openPath = "F:\\"
                    os.startfile(openPath)

                elif 'send email' in query:
                    try:
                        while True:
                            speck_fun("whom to send?")
                            name = takeCommand()
                            if name == "None":
                                pass
                            else:
                                break
                        speck_fun("What should I say?")
                        content = takeCommand()
                        to = email[name]
                        sendEmail(to, content)
                        speck_fun("Email has been sent!")
                    except Exception as e:
                        print(e)
                        speck_fun("Sorry my friend hemal bhai. I am not able to send this email")

                elif "play music" in query:
                    music_dir = 'F:\\New Songs\\Rahat Fateh Ali Khan - All Hit Songs'
                    songs = os.listdir(music_dir)
                    print(songs)
                    os.startfile(os.path.join(music_dir, songs[random.randint(0,songs.__len__()-1)]))


        else:
            pass
