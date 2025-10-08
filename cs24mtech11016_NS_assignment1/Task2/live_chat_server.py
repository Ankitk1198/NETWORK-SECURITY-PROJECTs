
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Creating TCP socket using IPv4 address

peers={}                                                                  # Dictionary for storing connected peers

# Server IP and its port number
ip_server = "127.0.0.1"
p_server = 12345

server_socket.bind((ip_server, p_server))                                 # Binding the server socket with its IP and Port number
server_socket.listen(10)                                                  # keeping server socket on listning mode for incoming connection
BUFFER_SIZE = 256 

def handle_client(c_socket,c_add):                                        # Function to communicate with the client 
    message = "HI I'm server.Can I know ur name and listening port"
    c_socket.sendall(message.encode())
    data = c_socket.recv(BUFFER_SIZE).decode()
    peers[data]=c_socket.getpeername()[0]
    print(f"{data} : {peers[data]}")                                      # Storing clients name along with there ip 
    message = f"{data} U registered successfully"
    c_socket.sendall(message.encode())
    while True:
        data = c_socket.recv(BUFFER_SIZE).decode()
        
        if(data=="SEND_PEERS"):                                            # To send list of peers if clients ask for it
            peer_list = "\n".join(f"{name}: {peers[name]}" for name in peers)
            c_socket.sendall(peer_list.encode())
        elif(data=="CLOSE"):
            c_socket.close()                                                         # Closing client socket 
            break
            

    

while True:
    c_socket,c_add=server_socket.accept()                                              # Accepting connection from client 
    client_thread = threading.Thread(target=handle_client, args=(c_socket,c_add))      # Creating a thread to handle client       
    client_thread.start()
    


  






    


  














       