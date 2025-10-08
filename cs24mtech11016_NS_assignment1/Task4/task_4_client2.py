import socket
import threading
import os
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Get p and g from environment variables
p = int(os.getenv("P", "23"))  # Example prime
g = int(os.getenv("Q", "5"))   # Example generator

BUFFER_SIZE = 256
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))

# Receive initial message from server
local_ip = client_socket.getsockname()[0]
local_port = client_socket.getsockname()[1]
print(local_ip)
print(local_port)

data = client_socket.recv(BUFFER_SIZE).decode()
print(f"You are connected to {host}")
print(f"{data}")

# Diffie-Hellman Key Exchange Functions
def generate_private_key():
    return random.randint(1, p - 1)

def generate_public_key(private_key):
    return pow(g, private_key, p)

def compute_shared_secret(public_key, private_key):
    return pow(public_key, private_key, p)

def derive_key(shared_secret):
    return hashlib.sha256(str(shared_secret).encode()).digest()

def encrypt_message(message, encryption_key):
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv=encryption_key[:16])
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext  # Prepend IV to ciphertext

def decrypt_message(ciphertext, encryption_key):
    iv = ciphertext[:16]
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return plaintext.decode()

def diffie_hellman_exchangeC(play_socket):
    play_socket.sendall(f"p:{p} g:{g}".encode())
    print(f"[Send]: p: {p} g: {g}")
    
    peer_public_key = int(play_socket.recv(BUFFER_SIZE).decode())
    print(f"[Received]: Peer Public Key: {peer_public_key}")

    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    
    print(f"[Send]: Public Key: {public_key}")
    play_socket.sendall(str(public_key).encode())  
    
    shared_secret = compute_shared_secret(peer_public_key, private_key)
    print(f"Shared Secret: {shared_secret}")
   
    encryption_key = derive_key(shared_secret)
    print(f"[Generated AES Key]: {encryption_key.hex()}")
    return encryption_key

def diffie_hellman_exchangeL(play_socket):
    data = play_socket.recv(BUFFER_SIZE).decode()
    print(f"[Received]: {data}")

    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
   
    print(f"[Send]: Public Key: {public_key}")
    play_socket.sendall(str(public_key).encode())  
    
    peer_public_key = int(play_socket.recv(BUFFER_SIZE).decode())
    print(f"[Received]: Peer Public Key: {peer_public_key}")
    
    shared_secret = compute_shared_secret(peer_public_key, private_key)
    print(f"Shared Secret: {shared_secret}")
   
    encryption_key = derive_key(shared_secret)
    print(f"[Generated AES Key]: {encryption_key.hex()}")
    return encryption_key

def send_client(play_socket, encryption_key):
    while True:
        try:
            message = input()
            if message == "EOD":
                print(f"[Plain_text]: {message}")
                encrypted_msg = encrypt_message(message, encryption_key)
                print(f"[SENT Cipher]: {encrypted_msg.hex()}")
                play_socket.sendall(encrypted_msg)
                play_socket.close()
                break
            else:
                print(f"[Plain_text]: {message}")
                encrypted_msg = encrypt_message(message, encryption_key)
                print(f"[SENT Cipher]: {encrypted_msg.hex()}")
                play_socket.sendall(encrypted_msg)
        except (BrokenPipeError, OSError):
            print("Connection lost while sending.")
            break

def receive_client(play_socket, encryption_key):
    while True:
        try:
            data = play_socket.recv(BUFFER_SIZE)

            if not data:
                print("Connection closed by peer.")
                break
            decrypted_msg = decrypt_message(data, encryption_key)
            if decrypted_msg == b"EOD":
                print(f"[Received Cipher_text]: {data}")
                print(f"[Decrypted Plain_text]: {decrypt_message}")
                print("Connection closed")
                break
            else:
                #decrypted_msg = decrypt_message(data, encryption_key)
                print(f"[Received Cipher]: {data.hex()}\n[Decrypted Plain]: {decrypted_msg}")
        except (ConnectionResetError, OSError):
            print("Peer disconnected unexpectedly.")
            break
    play_socket.close()
def r_peers():
    client_socket.sendall("SEND_PEERS".encode())
    data = client_socket.recv(BUFFER_SIZE).decode()
    print(data)

def l_fpeers():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_port = int(input("Enter listening port: "))
    new_socket.bind((local_ip, local_port))
    new_socket.listen(2)
    print("Listening for peer connection...")
    try:
        l_socket, l_add = new_socket.accept()
        print("You are connected to peer 1")
        encryption_key = diffie_hellman_exchangeL(l_socket)
        send_thread = threading.Thread(target=send_client, args=(l_socket, encryption_key))
        receive_thread = threading.Thread(target=receive_client, args=(l_socket, encryption_key))
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
        encryption_key = diffie_hellman_exchangeC(new_socket)
        send_thread = threading.Thread(target=send_client, args=(new_socket, encryption_key))
        receive_thread = threading.Thread(target=receive_client, args=(new_socket, encryption_key))
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
        print("Enter : 1 to know other peers' IP and port")
        print("Enter : 2 to listen from peer")
        print("Enter : 3 to connect to peer")
        print("Enter : 4 to close connection with server")
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
        except ValueError:
            print("Invalid input. Please enter a number.")
    break
