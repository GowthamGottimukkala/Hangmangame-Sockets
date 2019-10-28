import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
s.connect((socket.gethostname(), port))

full_msg = s.recv(1024).decode("utf-8")
print(full_msg)
tries = 5
while(tries):
	letter = input("Enter the letter:")
	s.send(bytes(letter,"utf-8"))
	word = s.recv(1024).decode("utf-8")
	print(word)
	t = s.recv(1024).decode("utf-8")
	tries = int(t)
	print("No.of tries left - ",tries)