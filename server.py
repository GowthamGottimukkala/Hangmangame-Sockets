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
tries = 5
string = "You have 5 tries to guess the word and win. Word length is "
clientsocket.send(bytes(string + str(len(word)),"utf-8"))
lis = []
while(tries):
    letter = clientsocket.recv(1024).decode("utf-8")
    print("Obtained letter is ", letter)
    if letter in word:
        lis.extend([k for k,char in enumerate(word) if char==letter])
        string = ""
        for i in range(len(word)):
            if i not in lis:
                string = string + "_ "
            else:
                string = string + word[i] + " "    
        string2 = string.replace(" ","")
        if(string2==word):
            print("He succeeded")
            string = string + "\nYOU WON !!!"
            tries = 0
        clientsocket.send(bytes(string,"utf-8"))        
        clientsocket.send(bytes(str(tries),"utf-8"))
    else:
        tries -= 1
        if(tries==0):
            string = "YOU KILLED HIM !!!"
        else:
            string = "You made a mistake."
        clientsocket.send(bytes(string,"utf-8"))
        clientsocket.send(bytes(str(tries),"utf-8"))

time.sleep(1)
clientsocket.close()