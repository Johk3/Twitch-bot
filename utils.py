import keys
import urllib2, json
import time, thread
from time import sleep


def chat(sock, msg):
    # Send a chat message to the server.
    sock.send("PRIVMSG #{} : {}\r\n".format(keys.chan, msg))


def ban(sock, user):
    # Just a ban function
    chat(sock, ".ban {}".format(user))


def timeout(sock, user, seconds=600):
    # A timeout
    chat(sock, ".timeout {}".format(user, seconds))


def threadFillOplist():
    while True:
        try:
            req = urllib2.Request(keys.CHECK, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                keys.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    keys.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    keys.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    keys.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    keys.oplist[p] = "staff"
        except Exception as e:
            print(e)
        sleep(5)


def isOp(user):
    return user in keys.oplist

