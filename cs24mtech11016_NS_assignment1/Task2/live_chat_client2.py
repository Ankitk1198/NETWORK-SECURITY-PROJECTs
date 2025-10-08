import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '192.168.0.140' 
port = 12345        
BUFFER_SIZE = 256

client_socket.connect((host, port))

# Receive initial message from server
local_ip = client_socket.getsockname()[0]
local_port = client_socket.getsockname()[1]
print(local_ip)
print(local_port)

data = client_socket.recv(BUFFER_SIZE).decode()
print(f"You are connected to {host}")
print(f"{data}")

def send_client(play_socket):
    while True:
        try:
            message = input()
            if message == "EOD":
                print(f"[send]: {message}")
                play_socket.sendall(message.encode())  # Notify peer before closing
                play_socket.close()
                break  # Exit loop safely
            else:
                print(f"[send]: {message}")
                play_socket.sendall(message.encode())
        except (BrokenPipeError, OSError):
            print("Connection lost while sending.")
            break  # Exit loop safely

def receive_client(play_socket):
    while True:
        try:
            data = play_socket.recv(BUFFER_SIZE).decode()
            if not data:
                print("Connection closed by peer.")
                break  # Exit loop safely
            if data == "EOD":
                print(f"[receive]: {data}")
                print("Connection closed")
                break  # Stop receiving after EOD
            else:
                print(f"[receive]: {data}")
        except (ConnectionResetError, OSError):
            print("Peer disconnected unexpectedly.")
            break  # Handle disconnections gracefully
    play_socket.close()  # Ensure socket is closed at the end

def r_peers():
    client_socket.sendall("SEND_PEERS".encode())
    data = client_socket.recv(BUFFER_SIZE).decode()
    print(data)

def l_fpeers():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_port=int(input("enter listening port"))
    new_socket.bind((local_ip, local_port))
    new_socket.listen(2)
    print("Listening for peer connection...")

    try:
        l_socket, l_add = new_socket.accept()
        print("You are connected to peer 1")
        l_socket.sendall("You are connected to peer2".encode())

        send_thread = threading.Thread(target=send_client, args=(l_socket,))
        receive_thread = threading.Thread(target=receive_client, args=(l_socket,))
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()
    except Exception as e:
        print(f"Error accepting peer connection: {e}")
    finally:
        new_socket.close()

def c_peer():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip_peer = input("Enter peer IP: ")
    p_peer = int(input("Enter peer port: "))

    try:
        new_socket.connect((ip_peer, p_peer))
        print(f"You are connected to {ip_peer}")

        send_thread = threading.Thread(target=send_client, args=(new_socket,))
        receive_thread = threading.Thread(target=receive_client, args=(new_socket,))
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()
    except Exception as e:
        print(f"Error connecting to peer: {e}")
    finally:
        new_socket.close()

while True:
    message = input("Enter your name and listening port to register at server: ")
    client_socket.sendall(message.encode())
    data = client_socket.recv(BUFFER_SIZE).decode()
    print(data)

    while True:
        print("Enter : 1 to know other peers ip and listening port")
        print("Enter : 2 to listen from peer")
        print("Enter : 3 to connect to peer")
        print("Enter : 4 to close connection with server")
        print("Enter other than above options to terminate completely")

        try:
            num = int(input())

            if num == 1:
                r_peers()
            elif num == 2:
                l_fpeers()
                
            elif num == 3:
                c_peer()
                
            elif num == 4:
                client_socket.sendall("CLOSE".encode())
                client_socket.close() 
            else:
                break
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    break