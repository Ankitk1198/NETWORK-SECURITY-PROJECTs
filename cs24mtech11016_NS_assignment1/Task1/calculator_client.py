import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Creating TCP socket using IPv4 address

host = '192.168.0.140'                   # Ip of server 
port = 12345                             # Port number of server
BUFFER_SIZE = 256                        

client_socket.connect((host, port))             # Requsting connection from server

data = client_socket.recv(BUFFER_SIZE).decode()
print(f"You are connected to {host}")              # Confirming connection with server
print(f"{data}")

while True:   
    message = input("Enter equation: ")            # Giving input for calculation
    client_socket.sendall(message.encode())

    data = client_socket.recv(BUFFER_SIZE).decode()     # Receiving output of that input equation
    print(f"RESULT: {data}")

    if data == "SERVER_SHUTDOWN":                      # After receiving SERVER_SHUTDOWN from server, socket will be closed
        client_socket.close()                        
        break  



