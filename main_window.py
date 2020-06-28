import asyncio
import socket
import re
import time
import aioconsole
from aioconsole import ainput




async def pinger(s):
    asyncio.sleep(60)
    millis = int(round(time.time() * 1000))
    # somehow look into how to only run this once
    # if(firstPong):
    #     s.send(bytes("JOIN "+ "#general" +"\n", "UTF-8"))
    #     firstPong = False
    s.send(bytes('PING LAG' + str(millis) + '\r\n', "UTF-8"))
    #print("ping sent!")

async def sender(s):


    s.send(bytes("PRIVMSG "+ "#general" +" :"+ line +'\r\n', "UTF-8"))




# async def some_function(s):
#
#
#     stripper = s.recv(2048).decode("UTF-8")
#     # if(stripper):
#     print(stripper)
#     stripper.strip('\n\r')

    # if stripper.find ( 'PING :' ) != -1:
    #     result = re.search("PING :+[0-9]*", stripper)
    #     fresh = result.group(0)
    #
    #     #print(fresh.strip("PING :"))
    #
    #
    #
    #     #s.send(bytes('PONG : ' + ":my.server.name" + '\r\n', "UTF-8"))
    #     s.send(bytes('PONG : ' + fresh.strip("PING :") + '\r\n', "UTF-8"))
    #     #s.send(bytes('PONG :' + fresh.strip("PING :") + '\n', "UTF-8"))
    #     print("pong sent")




async def forever():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 6667))
    botnick = "davekells"
    chan = "#general"
    # somewhere here we need to fix this so it can send byte code and this string for a IDENT otherwise
    # we cannot connect to the server
    s.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " " + botnick + "\n", "UTF-8"))
    s.send(bytes("NICK " + botnick + "\n", "UTF-8"))  # assign the nick to the bot
    s.send(bytes("JOIN "+ chan +"\n", "UTF-8"))


    asyncio.ensure_future(pinger(s))

    while True:
        stripper = s.recv(2048).decode("UTF-8")
        # if(stripper):
        stripper.strip('\n\r')
        print(stripper)

        #await sender(s)















loop = asyncio.get_event_loop()

loop.run_until_complete(forever())

#     s.send(bytes("JOIN "+ "#general" +"\n", "UTF-8"))

