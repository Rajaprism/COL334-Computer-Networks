import socket
import sys
import time

# Server information
server_ip = "10.17.7.218"
server_port = 9801

hathi_ip= "10.184.5.250"
# hathi_ip="10.194.28.208"
hathi_port =1235

stor  = [0]*1000

All_lines =["-37"]*1000

# Function to connect to the server
def connect_to_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print("connected to server")
        hathi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hathi_socket.connect((hathi_ip,hathi_port))
        print("connected to hathi")
        return client_socket , hathi_socket
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)

def receive(hathi_socket):
    for i in range(0,1000) :
        if stor[i]==1:
            continue
        else:
            hathi_socket.sendall(str(i).encode())
            line_buffer=""
            while True :
                parts = hathi_socket.recv(1024).decode()
                line_buffer+=parts
                if parts.endswith("\n"):
                    break
            All_lines[i]=line_buffer
            # print(i," clinet side ",line_buffer)
    hathi_socket.sendall("-1".encode())
    hathi_socket.close()

def submit(client_socket):
    print("Submission Started....")
    submit="SUBMIT\n"
    info ="cs1210915@bauxite\n"
    count ="1000\n"
    client_socket.sendall(submit.encode())
    client_socket.sendall(info.encode())
    client_socket.sendall(count.encode())
    for i in range(0,1000):
        # print(i)
        client_socket.sendall((str(i)+"\n").encode())
        client_socket.sendall(All_lines[i].encode())
        # print(All_lines[i])
    res=client_socket.recv(1024).decode()
    print(res)


# Function to send a SENDLINE request to the server
def send_sendline_request(client_socket,hathi_socket):
    x=0
    global hathi_ip
    global hathi_port
    try:
        request = "SENDLINE\n"
        # signal = hathi_socket.recv(1024).decode()
        # print(signal)
        while True :
            try:
                signal = hathi_socket.recv(1024).decode()
            except ConnectionResetError:
                print(f"Client disconnected. Reconnecting...")
                hathi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                hathi_socket.connect((hathi_ip,hathi_port))
                print(f"Reconnected to hathi")
                continue
            if(signal=="1"):
                line_buffer=""
                client_socket.sendall(request.encode())
                while True :
                    parts = client_socket.recv(1024).decode()
                    line_buffer += parts
                    if parts.endswith("\n"):
                        break
                # print(line_buffer.split('\n',1)[0])
                num = int(line_buffer.split('\n',1)[0])
                # print("from vayu ",line_buffer)
                if num == -1 or stor[num]==1:
                    line_buffer="-1\n"
                else:
                    stor[num]=1
                    All_lines[num]=line_buffer.split('\n',1)[1]
                try:
                    hathi_socket.sendall(line_buffer.encode())
                except ConnectionResetError:
                    print(f"Client disconnected. Reconnecting...")
                    hathi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    hathi_socket.connect((hathi_ip,hathi_port))
                    print(f"Reconnected to hathi")
                    continue

            else:
                receive(hathi_socket)
                print("received")
                submit(client_socket)
                break
    except Exception as e:
        print(f"Error sending SENDLINE request: {e}")
        return None, None

if __name__ == "__main__":
    client_socket,hathi_socket = connect_to_server()
    send_sendline_request( client_socket , hathi_socket )
    client_socket.close()
    # have = ["-23"]*1000
    # ct=1000
    # for i in range (0,1000):
    #     print(i , have[i])
    # while ct>0:
    #     # command=input()
    #     line = send_sendline_request(client_socket).split('\n',1)
    #     print(line)
    #     x=int(line[0])
    #     if have[x]=="-23" : 
    #         print(x)
    #         have[x]=line[1]
    #         ct-=1
    # print(have)
    # for i in range (0,1000):
    #     print(i , have[i][:5])
    # submit="SUBMIT\n"
    # info="cs1210917@bauxite"
    # client_socket.sendall(submit.encode())
    # client_socket.sendall(info.encode())
    # for i in range (0,1000):
    #     client_socket.sendall()