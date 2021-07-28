import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import mutagen
from mutagen.mp3 import MP3
import webbrowser as wb
import psutil
import pyjokes
import time

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 160)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1)
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[2].id)

def intro(audio = " Iam Friday. Your Personal Voice Assistant at your service."):
    engine.say(audio)
    engine.runAndWait()

def greet():
        hour = datetime.datetime.now().hour

        if hour >= 6 and hour < 12:
            intro("Good Morning. Have a nice day.")
        elif hour >= 12 and hour < 18:
            intro("Good Afternoon")
        elif hour >= 18 and hour < 21:
            intro("Good Evening")
        else:
            intro("Good Night. Have a sweet dreams.")

def current_time():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    intro("The current time is ")
    intro(time)

def current_date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    intro("The current date is ")
    intro(day)
    intro(month)
    intro(year)

def wikipedia_search(query):
    intro("searching in wikipedia")
    query = query.replace("wikipedia", "")
    result = wikipedia.summary(query, sentences = 5)

    if result:
        intro(result)
    else:
        intro("something went wrong. Please check your internet connection or I can't understand the words. Please say again.")

def chrome_search():
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" # Add your chrome path here
    intro("Opening the google chrome tab.")
    wb.register('chrome', None, wb.BackgroundBrowser(chrome_path))
    intro("What would you like to search.")
    search = command().lower()
    wb.get('chrome').open_new_tab(f"{search}.com")
    time.sleep(10)

def play_songs():
    intro("Starting to play songs")
    songs_dir = "D:\Music"  # Add you music directory path here
    songs = os.listdir(songs_dir)

    for song in range(len(songs)):
        start_song = os.path.join(songs_dir, songs[song])
        audio = MP3(start_song)
        duration = audio.info.length
        os.startfile(start_song)
        time.sleep(duration + 2)

        intro("Would you like to play next song")
        query = command().lower()

        if "no" in query:
            intro("Thanks for playing the songs. I think now your mood is good.")
            break
        else:
            intro("Playing the next song")
    else:
        intro("I think all the songs are played.")

def remember_task():
    print("What would you like to remember")
    intro("What would you like to remember")
    data = command().lower()
    intro(f"I think you asked me to remember: {data}")
    remember = open('remember.txt', 'a')
    remember.write(f"{data}.\n")
    remember .close()
    intro("Added to the remember list successfully")

def todo_task():
    print("The task you asked to remember is...")
    intro("The task you asked me to remember is ")
    remember = open('remember.txt', 'r')
    data = remember.read()

    if data:
        intro(data)
    else:
        intro("There is nothing in the todo list.")

def remove_task():
    intro("Would you like to delete the todo task")
    query = command().lower()

    if "yes" in query:
        if os.path.exists('remember.txt'):
            os.remove('remember.txt')
            intro("Delete the remember list successfully.")
        else:
            print("No such files found")
            intro("There is nothing in here.")

def cpu_usage():
    intro("Checking the CPU and Battery usage.")
    cpu_count = psutil.cpu_count()
    core_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=1)
    battery_usage = list(psutil.sensors_battery())
    battery_percent = battery_usage[0]
    power_pluged = battery_usage[2]
    frequency = list(psutil.cpu_freq(percpu=False))
    current_frequency = frequency[0]
    minimum_frequency = frequency[1]
    maximum_frequency = frequency[2]
    process = list(psutil.Process().io_counters())
    read_count = process[0]
    write_count = process[1]
    read_byte = process[2]
    write_byte = process[3]
    other_count = process[4]
    other_byte = process[5]

    intro(f"The total cpu physical core is {core_count}")
    intro(f"The total cpu physical core with multithreading is {cpu_count}")
    intro(f"The total CPU percentage in use is {cpu_percent}%")
    intro(f"The current battery percentage in your PC is {battery_percent}")

    if power_pluged:
        intro("You have been charging your device")
    else:
        intro("You have not plugged to the charger")

    intro(f"The current frequency of your CPU is {current_frequency}")
    intro(f"The minimum frequency of your CPU is {minimum_frequency}")
    intro(f"The maximum frequency of your CPU is {maximum_frequency}")
    intro(f"The number of read operation performed is {read_count}")
    intro(f"The number of write operation performed is {write_count}")
    intro(f"The number of bytes read operation is {read_byte}")
    intro(f"The number of bytes write operation is {write_byte}")
    intro(f"The number of operation performed other than read and write is {other_count}")
    intro(f"The number of bytes transferd during operation other than read and write is {other_byte}")

def jokes():
    joke = pyjokes.get_joke(language='en', category='all')
    intro(joke)

    intro("Would you like to hear other jokes")
    query = command().lower()

    if "yes" in query:
        jokes()
    else:
        intro("I think you have heard a great jokes. Thank you.")

def command():
    print("Listening")
    intro("Listening to you")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5)

        try:
            print("Recognizing")
            intro("Recognizing what you said")
            query = r.recognize_google(audio)
            print("I think you said {}".format(query).lower())
            intro("I think you said {}".format(query).lower())
        except Exception as e:
            print(e)
            query = "I can't able to understand your voice. Please say that again"
        return query


if __name__ == "__main__":
    greet()
    intro()
    while True:
        time.sleep(2)
        intro("How can I help you?")
        query = command().lower()

        if "time" in query:
            print("Time")
            current_time()
        elif "date" in query:
            print("Date")
            current_date()
        elif "wikipedia" in query:
            print("Wikipedia")
            wikipedia_search(query)
        elif "music" in query:
            print("Playing Music")
            play_songs()
        elif "search" in query:
            print("Searching...")
            chrome_search()
        elif "remember" in query:
            print("Remembering...")
            remember_task()
        elif "task" in query:
            print("Going to check the text document")
            todo_task()
        elif "remove" in query:
            print("Removing the todo task")
            remove_task()
        elif "usage" in query:
            print("CPU usage...")
            cpu_usage()
        elif "joke" in query:
            print("Jokes...")
            jokes()
        elif "logout" in query:
            print("Logging Out")
            os.system("shutdown - l")
        elif "shutdown" in query:
            print("Shutting Down")
            os.system("shutdown /s /t 1")
        elif "restart" in query:
            print("Restarting")
            os.system("shutdown /r /t 1")
        elif "hibernate" in query:
            print("Hibernate...")
            os.system("shutdown /h /t 1")
        elif "can't able to understand your voice. please say that again" in query:
            intro(query)
        elif "quit" or "stop" in query:
            print("Closing")
            quit()