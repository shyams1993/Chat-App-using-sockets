### Client side program that connects to the server code ###

#import the same set of libraries as imported in the server script
#additionally import Tkinter (Python's Stock GUI Module)
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

#function to handle receiving of messages
#endless loop while true
    #since we should be able to receive msgs whenever we want, we use an endless loop
    #The functionality within the loop is pretty straightforward; the recv() is the blocking part.
    #It stops execution until it receives a message, and when it does, we move ahead and append the message to msg_list
#decode the received msg (received as bytes) to UTF-8 characters and store in msg
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

#function to handle message sending
#event is being passed as an argument because as soon as send button is clicked, the function is invoked
# event is passed by binders.
#my_msg is the GUI's message field
    #used to get the messages and store it in msg variable
#then we clear the message field to type
    #if the msg isnt quit, broadcasts the message to all connected users(as seen in server function)
    #if it is, then closes the client connected and then closes the GUI App via Tkinter's top.close() function
def send(event=None):  
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


#function that's called when the window is closed
#clean up before closing GUI app and thus terminating the client's connection to the socket
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

#Main function that uses Python's Tkinter
#we create a variable top that calls Tkinter with Tk() as an object
#we also name the title bar
top = tkinter.Tk()
top.title("Sutherland's Chat App")


#now we create a frame to hold the messages and call top as an argument
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  #For the messages to be sent.
my_msg.set("Type your messages here.") #setting the placeholder text in the input box
scrollbar = tkinter.Scrollbar(messages_frame)  #Scrollbar to navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=20, width=100, yscrollcommand=scrollbar.set) #listbox specifying the message frame dimensions and scrollbar (Y-axis because of vertical list)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) #defining the position of scrollbar by calling scrollbar.pack() and defining to occupy right side
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH) #similarly defining the position of msgs by called msg_list.pack() and defining to occupy left side
msg_list.pack()         #finally packing msg.list and message_frame
messages_frame.pack()   #packing entire messages_frame using .pack() function

#now we create the input field to type the messages and define it to hold "my_msg" variable which contains the user msg
entry_field = tkinter.Entry(top, textvariable=my_msg) 
#also binding it to the send function so that whenever the user presses return, the message is sent to the server
entry_field.bind("<Return>", send)
#packing that as well within the GUI
entry_field.pack()
#creating a send button and mapping it to the send function
send_button = tkinter.Button(top, text="Send", command=send)
#packing that as well
send_button.pack()
#finally the cleanup function on_closing() which should be called when the user wishes to close the GUI window
top.protocol("WM_DELETE_WINDOW", on_closing)

#the code logic that actually connects to the server
#creating a variable HOST that asks the user the host IP/hostname where the server resides
HOST = input('Enter host: ')
#similarly PORT variable has been created to get the Port number as input
    #if user inputs any other port except specified one, we pass the default one as the port number we specified on the server script
    #else take user input as port but error will popup
PORT = input('Enter port: ')
if not PORT:
    PORT = 8080
else:
    PORT = int(PORT)

#specifying the same constants: BUFSIZE as 1024 & ADDR as a combo of HOST and PORT
BUFSIZ = 1024
ADDR = (HOST, PORT)

#create the client socket to connect to the server by creating clientsocket variable
#client socket variable uses socket as an object that takes Internet Address Family(type of AF) & mode of socket communication(here SOCK_STREAM because its TCP || If UDP, would have been SOCK_DGRAM)
client_socket = socket(AF_INET, SOCK_STREAM)
#connect to the address by calling connect function
client_socket.connect(ADDR)

#initiate thread by calling receive action passed as an argument via target argument
receive_thread = Thread(target=receive)
#Starts GUI execution.
receive_thread.start()

tkinter.mainloop()  


### END OF CODE ###
