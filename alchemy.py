import ssl
import socket
import time
import select
import random

HOST = "irc.pdgn.co"
PORT = 6697
CHAN = "#pdgn"
NICK = "alchemy"
SSL = True

raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if SSL:
    s = ssl.wrap_socket(raw)
else:
    s = raw

s.connect((socket.gethostbyname(HOST), PORT))
print s.recv(1024)

def send(x):
    s.send(x+"\r\n")

def display(x):
    send("PRIVMSG %s :%s"%(CHAN, x))


send("NICK %s"%(NICK))
send("USER %s 0 * %s"%(NICK, NICK))


while True:
    x = s.recv(1024)
    print x,
#    if "PING" in x:
#        send("PONG :" + x[7:])
#        send("VERSION")
#        print "PONG :" + x[6:]
#        break
    if "onn" in x:
        break

send("JOIN %s"%(CHAN))
def pong():
    send("PONG") # lord of the pings

f = open("progress.txt")
collection = set(map(lambda x: x[:-1], f.readlines()))
f.close()

#collection = set(["water", "air", "fire", "earth"])
pairs = [
    ("water", "air", "cloud"),
    ("cloud", "water", "rain"),
    ("rain", "earth", "soil"),
    ("ice", "energy", "frozone"),
    ("fire", "fire", "energy"),
    ("fire", "water", "steam"),
    ("fire", "earth", "lava"),
    ("lava", "water", "stone"),
    ("stone", "man", "neanderthal"),
    ("fire", "man", "fireman"),
    ("energy", "soil", "plant"),
    ("energy", "energy", "light"),
    ("tool", "fireman", "axe"),
    ("light", "light", "sentience"),
    ("sentience", "air", "pidgeon"),
    ("pidgeon", "evil", "pidgey"),
    ("sentience", "earth", "man"),
    ("sentience", "man", "evil"),
    ("plant", "rain", "tree"),
    ("tree", "energy", "ent"),
    ("ent", "sentience", "treebeard"),
    ("evil", "man", "villain"),
    ("cloud", "energy", "lightning"),
    ("lightning", "earth", "electricity"),
    ("air", "energy", "wind"),
    ("wind", "soil", "sandstorm"),
    ("wind", "wind", "tornado"),
    ("cloud", "cloud", "thunder"),
    ("earth", "wind", "mountain"),
    ("snow", "tree", "christmas"),
    ("water", "energy", "tsunami"),
    ("christmas", "man", "santa"),
    ("stone", "fire", "metal"),
    ("metal", "steam", "engine"),
    ("engine", "water", "boat"),
    ("water", "water", "ocean"),
    ("tool", "metal", "sculpture"),
    ("sculpture", "sentience", "robot"),
    ("robot", "evil", "jacob"),
    ("tool", "earth", "hole"),
    ("hole", "water", "pool"),
    ("pool", "man", "backstroke"),
    ("boat", "ocean", "ship"),
    ("ship", "energy", "starship"),
    ("ship", "sentience", "kitt"),
    ("metal", "water", "rust"),
    ("rust", "man", "aaron"),
    ("man", "sentience", "genius"),
    ("genius", "energy", "science"),
    ("man", "tree", "wood"),
    ("man", "metal", "tool"),
    ("wood", "tool", "house"),
    ("house", "sentience", "pat"),
    ("cloud", "genius", "meatball"),
    ("metal", "electricity", "computer"),
    ("computer", "sentience", "hal"),
    ("hal", "man", "google"),
    ("tool", "soil", "crops"),
    ("crops", "rain", "food"),
    ("food", "man", "restaurant"),
    ("evil", "genius", "megamind"),
    ("google", "cloud", "internet"),
    ("man", "internet", "hacker"),
    ("hacker", "evil", "blackhat"),
    ("blackhat", "sentience", "xkcd"),
    ("metal", "fire", "sword"),
    ("sword", "light", "lightsaber"),
    ("man", "sword", "knight"),
    ("knight", "sentience", "chivalry"),
    ("chivalry", "hacker", "whitehat"),
    ("metal", "metal", "noise"),
    ("noise", "genius", "music"),
    ("music", "genius", "bach"),
    ("music", "sandstorm", "darude"),
    ("bach", "hacker", "hofstader"),
    ("music", "computer", "dubstep"),
    ("music", "metal", "rock"),
    ("rock", "genius", "beatles"),
    ("rain", "light", "rainbow"),
    ("rainbow", "rainbow", "joy"),
    ("joy", "hacker", "python"),
    ("genius", "hacker", "mel"),
    ("water", "wind", "ice"),
    ("ice", "water", "snow"),
    ("snow", "man", "snowman"),
    ("snowman", "sentience", "olaf"),
    ("olaf", "fire", "puddle"),
    ("olaf", "music", "letitgoooooo"),
    ("snow", "sentience", "penguin"),
    ("penguin", "hacker", "linux"),
    ("linux", "internet", "server"),
    ("server", "man", "sysadmin"),
    ("sysadmin", "joy", "coffee"),
    ("coffee", "hacker", "stallman"),
    ("stallman", "computer", "foss"),
    ("man", "joy", "love"),
    ("foss", "hacker", "bug"),
    ("bug", "blackhat", "exploit"),
    ("exploit", "earth", "lifehack"),
    ("sysadmin", "evil", "ninja"),
    ("genius", "hofstader", "knuth"),
    ("knuth", "foss", "tex"),
]

def combine(a, b):
    for p in pairs:
        if (a == p[0] and b == p[1]) or (a == p[1] and b == p[0]):
            return p[2]
    return False

buf = ''
while True:
    pong()
    try:
        readables, writables, exceptionals = select.select([s], [s], [s])
        if len(readables) == 1:
            buf += s.recv(512)
            if buf[-2:] == '\r\n':
                messages = buf.split('\r\n')
                buf = ''
                for m in messages:
                    message = m.split(" ")
                    if len(message) > 2 and message[1] == "PRIVMSG" and message[2] == CHAN:
                        text = m.split(":")[2]
                        if len(text) > 1 and text[0] == "@":
                            elements = text[1:].split(" ")
                            if len(elements) == 1 and elements[0] == "help":
                                display("To mix a new brew: `@combine <element> <element>`")
                                display("To list your elements: `@list`")
                                display("Also try `@encourage` and `@hint`.")
                            elif len(elements) == 1 and elements[0] == "status":
                                display("Alive and happy. Thanks for asking.")
                            elif len(elements) > 1 and elements[0] == "encourage":
                                display(random.choice([
                                    "I love you, %s.",
                                    "It's for your own good, %s.",
                                    "Hey, %s, did you know that being utterly lost builds character?",
                                    "Everything's gonna be alright, %s.",
                                    "Cheer up, %s, it's only a game..",
                                    "I believe in %s.",
                                    "We all believe in %s.",
                                    "%s rocks!"
                                ])%(elements[1]))
                            elif len(elements) == 1 and elements[0] == "hint":
                                if random.random() < 0.9:
                                    display(random.choice(["No can do, buddy.", "Not this time!", "You'll be happier if you get it yourself."]))
                                else:
                                    c = random.choice(pairs)
                                    display("Hint: It's possible to make %s!"%(c[2]))
                            elif len(elements) == 1 and elements[0] == "list":
                                def chunks(l, n):
                                    for i in xrange(0, len(l), n):
                                        yield l[i:i+n]
                                for k in chunks(list(collection), 20):
                                    display("You have: %s"
                                        %", ".join(k))
                                display("That's %d out of %d!"%(len(collection), len(pairs)))
                            elif len(elements) == 3 and elements[0] == "combine":
                                e1 = elements[1].lower()
                                if e1 not in collection:
                                    display("You don't have %s!"%(e1))
                                    break
                                e2 = elements[2].lower()
                                if e2 not in collection:
                                    display("You don't have %s!"%(e2))
                                    break
                                if combine(e1, e2):
                                    if combine(e1, e2) in collection:
                                        display("You already combined %s and %s to get %s."%(e1, e2, combine(e1, e2)))
                                    else:
                                        display("You just discovered %s (%s + %s)!"
                                            %(combine(e1, e2), e1, e2))
                                        collection.add(combine(e1, e2))
                                        f = open("progress.txt", "w")
                                        f.write("\n".join(collection)+"\n")
                                        f.close()
                                else:
                                    display("%s and %s don't make anything exciting."%(e1, e2))
    except KeyboardInterrupt:
        send("PART %s :So long, and thanks for all the fish."%(CHAN))
        exit(0)
