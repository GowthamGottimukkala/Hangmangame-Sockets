import socket
import time
import sys
import threading
from random import randint
import os

t = [None,None]
s = [None,None]
clientsocket = [None,None]
tries = [4,4]
lisindex = [[],[]]
lisletter = [[],[]]
letter = [None,None]
recword = [None,None]
initial = [None,None]
final = [None,None]
timetaken = [None,None]
completestatus = [9,9]
files = list(filter(lambda x: x.endswith('.txt'), os.listdir()))
file_in = files[randint(0, len(files) - 1)]
with open(file_in, 'r') as f:
    words = f. readlines()
words = [i.strip() for i in words]
category = words[0].upper()
word = words[randint(1, len(words) - 1)]
word = word.lower()
answer = ["",""]
def runner(s,clientsocket,i):
    initial[i] = time.time()
    spaces = []
    spaces = [str(i) for i,x in enumerate(word) if x==" "]
    first = str(len(word)) + ";" + ",".join(spaces)
    clientsocket.send(bytes(first,"utf-8"))
    time.sleep(0.2)
    clientsocket.send(bytes(category,"utf-8"))

    while(tries[i]):
        letter[i] = clientsocket.recv(1024).decode("utf-8")
        print("Obtained letter is ",letter[i])
        if letter[i] in word:
            lisindex[i].extend([str(k) for k,char in enumerate(word) if char==letter[i]])
            lisletter[i].extend([char for k,char in enumerate(word) if char==letter[i]])
            clientsocket.send(bytes(",".join(lisindex[i]),"utf-8"))
            time.sleep(0.2)
            clientsocket.send(bytes("".join(lisletter[i]),"utf-8"))
        else:
            clientsocket.send(bytes("no","utf-8"))
            time.sleep(0.2)
            clientsocket.send(bytes("no","utf-8"))
        time.sleep(0.2)
        if(tries[1-i]==0 and completestatus[1-i]==0):
            clientsocket.send(bytes("Opponent failed, You are the only hope","utf-8"))
        if(tries[1-i]==0 and completestatus[1-i]==1):
            clientsocket.send(bytes("Opponent saved the hangman","utf-8"))
        else:
            clientsocket.send(bytes("Opponent guessed " + str(len(lisletter[1-i])) + " letters","utf-8"))
        
        recword[i] = clientsocket.recv(1024).decode("utf-8")
        if(recword[i]==word):
            clientsocket.send(bytes("yes","utf-8"))
        else:
            clientsocket.send(bytes("no","utf-8"))
        completed = clientsocket.recv(1024).decode("utf-8")
        if(completed=="completed"):
            if(completestatus[1-i]==1):
                answer[i] = "but opponent is faster"
            else:
                answer[i] = "You won"
            completestatus[i] = 1
            tries[i] = 0
            final[i] = time.time()
            timetaken[i] = final[i] - initial[i]
            print(timetaken[i])
            print("Player-",i+1," completed")
            clientsocket.send(bytes("You guessed in " + str(timetaken[i]) + " units","utf-8"))
            time.sleep(0.2)
            clientsocket.send(bytes("You guessed, " + answer[i],"utf-8"))
        elif(completed=="notcompleted"):
            completestatus[i] = 0
            tries[i] = 0
            final[i] = time.time()
            timetaken[i] = final[i] - initial[i]
            clientsocket.send(bytes("You were unable to guess. You took " + str(timetaken[i]) + " units","utf-8"))
            time.sleep(0.2)
            clientsocket.send(bytes("GAME OVER, Answer: " +word,"utf-8"))
        else:
            clientsocket.send(bytes("Continuing..","utf-8"))
        time.sleep(0.2)
    time.sleep(1)
    clientsocket.close()



i = 0
while(True):
    s[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    if(i==0):
        port = int(sys.argv[1])
    else:
        port = port + 1
    s[i].bind(('', port))
    print("Socket binded to",port)
    s[i].listen(5)
    print("Socket listening")
    clientsocket[i], address = s[i].accept()
    i = i + 1
    print(f"Connection from {address} has been established.")
    if(i==2):
        break

for i in range(2):
    t[i] = threading.Thread(target=runner,args=(s[i],clientsocket[i],i))    
    t[i].start()

for i in range(2):
    t[i].join()

winner = timetaken.index(min(timetaken))+1
print("The Winner is ",winner)