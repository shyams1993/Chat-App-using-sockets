### Server side program to accept user connections to chat ###

#A socket is an internal endpoint for sending/receiving data within a node on a Network
#Using sockets, we import the AF_INET(Internet Address Family), socket(for communication) & sock_stream(TCP based Sockets)
    #why we use TCP (Sock_stream) & not UDP(sock_dgram) is because UDP is more suitable for Telephony
    #while for chats, TCP is most suitable
        #TCP (SOCK_STREAM) is a connection-based protocol. The connection is established and the two parties have a conversation until the connection is terminated by one of the parties or by a network error.
        #UDP (SOCK_DGRAM) is a datagram-based protocol. You send one datagram and get one reply and then the connection terminates.
            #UDP sockets because they’re more telephonic, where the recipient has to approve the incoming connection before communication begins
from socket import AF_INET, socket, SOCK_STREAM

#Using thread to initiate multiple threads within a session (each user connects = a thread)
#to facilitate multiple users, threading helps create appropriate threads
    #threading is just a higher level module that interfaces thread.
from threading import Thread

#creating a couple of constants for future use (Can be made dynamic as well)
clients = {}        #to collect the number of clients connected
addresses = {}      #to collect the client IP addresses

HOST = ''           #variable to store the Host IP that the Client would like to connect (Server address)
PORT = 8080         #port setup as constant
BUFSIZ = 1024       #buffer size initially set as 1024 (may need to change it to 2048)
ADDR = (HOST, PORT) #ADDR variable will be accepted as a combo of IP Address & Port number

SERVER = socket(AF_INET, SOCK_STREAM) #SERVER variable uses socket as an object that takes Internet Address Family(type of AF) & mode of socket communication(here SOCK_STREAM because its TCP || If UDP, would have been SOCK_DGRAM)
SERVER.bind(ADDR)   #server variable calls bind function to bind HOST and PORT stored in ADDR var


#Function to accept incoming connections
#This is just a loop that waits forever for incoming connections and as soon as it gets one, it logs the connection (prints some of the connection details) and sends the connected client a welcome message. 
#Then it stores the client’s address in the addresses dictionary and later starts the handling thread for that client.
#handle_client function hasn't been defined yet (next function in line)
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#Function to handle client communication (#Takes client socket as argument || #Handles single client only)
#gets the name and stores as argument of buffer_size(packets received over Ethernet) & decodes the bytes into UTF-8 character
#uses the name to print a welcome message
#sends it over as bytes
def handle_client(client):  
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
#an endless loop to ensure the text input(msg input) isn't quit,
    #as long as it isn't, gets the msg and displays the msg
    # if it is quit, quits the conversation and displays the convo
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

#Function to broadcast message content to all of them in the room
#prefix is for name identification.
#a for loop to send the message to all clients as bytes encoded into UTF-8 (Unicode Transformation Format (8 represent bit format))
#prepends an optional prefix if necessary. 
    #We do pass a prefix to broadcast() in our handle_client() function, and we do it so that people can see exactly who is the sender of a particular message
def broadcast(msg, prefix=""):  
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


#main function to start the server, listen for connections 
#for now, listens to maximum of 5 clients only (can change it as per requirement)
#accept incoming connections and start if we have IP and Port
#We join() ACCEPT_THREAD so that the main script waits for it to complete and doesn’t jump to the next line, which closes the server.
#closes the connection after user sends quit command
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

### END OF CODE ###
