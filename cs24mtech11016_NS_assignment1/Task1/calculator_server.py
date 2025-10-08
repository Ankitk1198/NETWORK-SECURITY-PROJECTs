
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creating TCP socket using IPv4 address

# Server IP and its port number
ip_server = "127.0.0.1"        
p_server = 12345


server_socket.bind((ip_server, p_server))        # Binding the server socket with its IP and Port number
server_socket.listen(5)                          # keeping server socket on listning mode for incoming connection
BUFFER_SIZE = 256 



# Function for calculating equation based on operators 
def calculate(op_1,op_2,oper):
   if(oper=="*"):
       return float(op_1) * float(op_2)
   elif(oper=="/"):
       return float(op_1) / float(op_2)
   elif(oper=="%"):
        return float(op_1) % float(op_2)
   elif(oper=="+"):
       return float(op_1) + float(op_2)
   elif(oper=="-"):
       return float(op_1) - float(op_2)
  

# Function to parse the equation 
def listing(n_data):
   e_list=[]
   oper=""                                  # To hold the current number or operand
   for char in n_data:
       if char.isdigit():
           oper+=char
       elif char in "*/%+-":
           if oper != "":
                e_list.append(oper)
                oper=""                   # Reset the operand
           e_list.append(char)            # Adding the operator to list
           oper=""
       elif char==" " and oper:
           e_list.append(oper)            # Adding the operand to list 
           oper=""
       elif char==".":
           oper+=char
   if oper:
       e_list.append(oper)


   return e_list


c_socket, c_add = server_socket.accept()          # Accepting connection from client 
print(f"Server is connected to: {c_add}")


with c_socket:                                                    # Communicating with the client
   message = "HI I'm server.I can solve equationsr"
   c_socket.sendall(message.encode())


   while True:
       data = c_socket.recv(BUFFER_SIZE).decode()
    
       if data == "END":                                           # If client sends END then Connection shut down
           print(f"client sent {data} connection request")
           c_socket.sendall(b"SERVER_SHUTDOWN")
           c_socket.close()                                        # Closing client socket 
           server_socket.close()                                   # Closing server socket 
           break  


       e_list=listing(data)                             # Listing received equation
    
       i=1
       k=len(e_list)-2
       while(k>0):
           if e_list[i] in "*/%":                               # Prioritising *,/ and % above others 
                e_list[i-1]=str(calculate(e_list[i-1],e_list[i+1],e_list[i]))
                del e_list[i]
                del e_list[i]
                k=k-2
           else:
                i=i+1
                k=k-1
       

       for item in e_list:
           print(item)

        
       i=1  
       k=int(len(e_list)/2)
       while(k>0):
           if e_list[i] in "+-":                             # Prioritising + and - below others
                e_list[i-1]=str(calculate(e_list[i-1],e_list[i+1],e_list[i]))
                del e_list[i]
                del e_list[i]
                k=k-1
           else:
                
                k=k-1
       for item in e_list:
           print(item)                                        # Printing the final result
       c_socket.sendall(str(e_list[0]).encode())              # Sending calculated result to client 









       