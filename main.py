import os
import sys

import speech_recognition as sr
import pyttsx3
import webbrowser
import openai

from config import apikey

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Shivam: {query}\n Jarvis: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt : {prompt} \n **************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'english+f3')
    engine.setProperty('rate', 120)
    engine.say(text)

    engine.runAndWait()


# def say(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust the energy threshold level based on the noise level in your environment
        r.energy_threshold = 4000
        r.pause_threshold = 0.8
        try:
            print("Listening....")
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            return query
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""


if __name__ == '__main__':
    print('PyCharm')
    say("Hello Shivam, I am Manvi AI your virtual wizard.")
    while True:
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["linkedin", "https://www.linkedin.com"],
                 ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir.....")
                browser = webbrowser.get()
                browser.open(site[1])

        if "open music" in query:
            musicPath = "/home/node_sm/Downloads/Another Love(Maddj.in).mp3"
            os.system(f'xdg-open "{musicPath}"')

        elif "open vs code" in query:
            filePath = "/snap/bin/code"
            os.system(f'"{filePath}"')

        elif "Using Artificial Intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Manvi Quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat reseted.")
        else:
            print("chatting........")
            chat(query)
