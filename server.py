import socket
import time
import sys
import threading

t = [None,None]
s = [None,None]
clientsocket = [None,None]
tries = [4,4]
category = "Songs"
lisindex = [[],[]]
lisletter = [[],[]]
letter = [None,None]
word = "karthik chowdary paladagu"
recword = [None,None]
word = word.lower()
initial = [None,None]
final = [None,None]
timetaken = [None,None]

def runner(s,clientsocket,i):
    # word = input("Enter the input word for player-{i}",)
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
        clientsocket.send(bytes("He guessed " + str(len(lisletter[1-i])) + " letters and have " + ,"utf-8"))
        recword[i] = clientsocket.recv(1024).decode("utf-8")
        if(recword[i]==word):
            clientsocket.send(bytes("yes","utf-8"))
        else:
            clientsocket.send(bytes("no","utf-8"))
        completed = clientsocket.recv(1024).decode("utf-8")
        if(completed=="completed"):
            tries[i] = 0
            final[i] = time.time()
            timetaken[i] = final[i] - initial[i]
            clientsocket.send(bytes("You guessed in " + str(timetaken[i]) + " units","utf-8"))
        elif(completed=="notcompleted"):
            tries[i] = 0
            final[i] = time.time()
            timetaken[i] = final[i] - initial[i]
            clientsocket.send(bytes("You were unable to guess. You took " + str(timetaken[i]) + " units","utf-8"))
        else:
            clientsocket.send(bytes("Continuing..","utf-8"))
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

print("The Winner is ",timetaken.index(min(timetaken))+1)
