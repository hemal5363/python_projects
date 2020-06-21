from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")

def speck_fun(str):
    print(str)
    speak.Speak(str)

import requests
url = ('https://newsapi.org/v2/top-headlines?country=in&apiKey=fcf0d47a152244d58eb2fe30e3f65232')

response = requests.get(url)
news = response.json()
stut = news['articles']

for i in stut:
    # if(i['source']['name']=="India.com"):
    str1 = f"news chanal name is {i['source']['name']}"
    speck_fun(str1)
    str2 = f"author name is {i['author']}"
    speck_fun(str2)
    str3 = f"news title is {i['title']}"
    speck_fun(str3)
    str4 = f"news description is {i['description']}"
    speck_fun(str4)


# print(news)
# # speck_fun(news)