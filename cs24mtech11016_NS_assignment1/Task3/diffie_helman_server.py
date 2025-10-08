
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peers={}

ip_server = "192.168.0.140"
p_server = 12345

server_socket.bind((ip_server, p_server))
server_socket.listen(10)   #setting queue size of 10 
BUFFER_SIZE = 256

def handle_client(c_socket,c_add):
    message = "HI I'm server.Can I know ur name and listening port"
    c_socket.sendall(message.encode())
    data = c_socket.recv(BUFFER_SIZE).decode()
    peers[data]=c_socket.getpeername()[0]                      #storing ip of connected client into key .here: key is the name and port number that client want to listen for other peers
    print(f"{data} : {peers[data]}")
    message = f"{data} U registered successfully"
    c_socket.sendall(message.encode())
    while True:
        data = c_socket.recv(BUFFER_SIZE).decode()
        
        if(data=="SEND_PEERS"):
            peer_list = "\n".join(f"{name}: {peers[name]}" for name in peers)      # on SEND PEERS request sending all clients registered on server
            c_socket.sendall(peer_list.encode())
        elif(data=="CLOSE"):
            c_socket.close()
            break
            

    

while True:
    c_socket,c_add=server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(c_socket,c_add))     #thread to handle multiple client
    client_thread.start()
    


  
