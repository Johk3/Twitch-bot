import keys
import utils
import socket
import re
import time
import thread
from time import sleep
import pyttsx


def main():
    # Networking functions
    engine = pyttsx.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice)
        engine.setProperty(voice, voice.id)  # changes the voice
        engine.say('Ready')
    engine.say("I am regy")
    engine.runAndWait()
    s = socket.socket()
    s.connect((keys.HOST, keys.PORT))
    s.send("PASS {}\r\n".format(keys.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(keys.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(keys.chan).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "All set up")

    thread.start_new_thread(utils.threadFillOplist, ())

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print response

            if message.strip() == "!time" and utils.isOp(username):
                utils.chat(s, "It's currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))

            if "!say" in message.strip():
                engine.say(re.sub('!say ', '', message.strip()))
                engine.runAndWait()

            if message.strip() == "!help":
                utils.chat(s, "!say, !time")

            if message.strip() == "!help" and utils.isOp(username):
                utils.chat(s, "!say, !time, !ban, !timeout")
        sleep(1)


if __name__ == '__main__':
    main()