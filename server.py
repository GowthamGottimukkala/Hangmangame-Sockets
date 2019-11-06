import socket
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")
port = int(sys.argv[1])
s.bind(('', port))
print("Socket binded to",port)
s.listen(5)
print("Socket listening")

clientsocket, address = s.accept()
print(f"Connection from {address} has been established.")

#Hangman starts
word = input("Enter the word:")
tries = 4
category = "songs"
clientsocket.send(bytes(str(len(word)),"utf-8"))
time.sleep(1)
clientsocket.send(bytes(category,"utf-8"))

lisindex = []
lisletter = []

while(tries):
    letter = clientsocket.recv(1024).decode("utf-8")
    print("Obtained letter is ",letter)
    if letter in word:
        lisindex.extend([str(k) for k,char in enumerate(word) if char==letter])
        lisletter.extend([char for k,char in enumerate(word) if char==letter])
        clientsocket.send(bytes("".join(lisindex),"utf-8"))
        time.sleep(1)
        clientsocket.send(bytes("".join(lisletter),"utf-8"))
    else:
        clientsocket.send(bytes("no","utf-8"))
        time.sleep(1)
        clientsocket.send(bytes("no","utf-8"))

    recword = clientsocket.recv(1024).decode("utf-8")
    if(recword==word):
        clientsocket.send(bytes("yes","utf-8"))
    else:
        clientsocket.send(bytes("no","utf-8"))
    # completed = clientsocket.recv(1024).decode("utf-8")
    # if(completed=="completed"):
    #     tries = 0

time.sleep(1)
clientsocket.close()