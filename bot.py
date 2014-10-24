#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Import some necessary libraries.
import socket
import subprocess

# Some basic variables used to configure the bot
server = "chat.freenode.net"  # Server
channel = "#makinacorpus"  # Channel
botnick = "raspoutine-test"  # nickname


def ping():  # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :Pong\n")


def sendmsg(chan, msg):  # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")


def joinchan(chan):  # This function is used to join channels.
    ircsock.send("JOIN " + chan + "\n")


def hello():  # This function responds to a user that inputs "Hello Mybot"
    ircsock.send("PRIVMSG " + channel + " :Hello!\n")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))  # Here we connect to the server using port 6667
ircsock.send("USER " + botnick + " " + botnick + " " + botnick + " :Makina bot\n")  # user authentication
ircsock.send("NICK " + botnick + "\n")  # here we actually assign the nick to the bot

joinchan(channel)  # Join the channel using the functions we previously defined

listen = False

while 1:  # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
    print(ircmsg)  # Here we print what's coming from the server

    # Begin to listen only when MOTD is done
    if ircmsg.find(":End of /MOTD command") != -1:
        listen = True
        continue

    if ircmsg.find(":Hello " + botnick) != -1:  # If we can find "Hello Mybot" it will call the function hello()
        hello()

    if ircmsg.find("PING :") != -1:  # if the server pings us then we've got to respond!
        ping()

    if ircmsg.find("PRIVMSG raspoutine-test :reload") != -1:
        # Fetch latest commits
        subprocess.call(["git", "fetch"])

        # See if we have changes
        commits = subprocess.check_output(["git", "log", "HEAD...master", "--pretty-format:%b"])

        # Pull latest content
        subprocess.call(["git", "pull"])
        # Reload script
        execfile(__file__)
