import socket
from _thread import *
import time

myserver_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
myserver_host="10.184.21.237"
myserver_port=1235

sirserver_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sirserver_host="10.17.7.218"
sirserver_port=9803

myserver_socket.bind((myserver_host,myserver_port))
myserver_socket.listen(5)

sirserver_socket.connect((sirserver_host,sirserver_port))

ThreadCount=0
Clients_list=[]
All_lines=["-69"]*1000
ct=1000
nclients=1
check=[0]*nclients

# limit = 500

def submit():
    print("Submission Started....")
    submit="SUBMIT\n"
    info ="cs1210915@bauxite\n"
    count ="1000\n"
    sirserver_socket.sendall(submit.encode())
    sirserver_socket.sendall(info.encode())
    sirserver_socket.sendall(count.encode())
    for i in range(0,1000):
        sirserver_socket.sendall((str(i)+"\n").encode())
        sirserver_socket.sendall(All_lines[i].encode())
    res=sirserver_socket.recv(1024).decode()
    print(res)
    k = res.replace('-', ',').split(',')
    st, en = int(k[-3]), int(k[-1])
    # print((en-st)/100000)

def Send_To_Clients(client_socket,threadno):
    print("sending to client has started")
    while True:
        # line_number = client_socket.recv(1024).decode()
        try:
            line_number = client_socket.recv(1024).decode()
        except ConnectionResetError:
            print(f"Client disconnected. Reconnecting...")
            client_socket, addr = myserver_socket.accept()
            Clients_list[threadno] = [client_socket, addr]
            print(f"Reconnected to client {threadno}")
            client_socket.send(bytes("0",'utf-8'))
            continue
        if line_number is None:
            continue
        line_number=int(line_number)
        if(line_number==-1):
            break
        payload=All_lines[line_number]
        client_socket.sendall(payload.encode('utf-8'))

def send_sendline_request(sirserver_socket):
    try:
        request = "SENDLINE\n"
        sirserver_socket.sendall(request.encode())
        line_buffer=""
        while True:
            line_number = sirserver_socket.recv(4096).decode()
            line_buffer +=line_number
            if line_number.endswith("\n"):
                break
        return line_buffer
    except Exception as e:
        print(f"Error sending SENDLINE request: {e}")
        return None, None

def client_thread(client_socket,threadno):
    # client_socket.send(bytes("Welcome to the server",'utf-8'))
    global ct
    lt=0
    while True:
        if(ct<=0):
            client_socket.send(bytes("0",'utf-8'))
            Send_To_Clients(client_socket,threadno)
            break
        else:
            client_socket.send(bytes("1",'utf-8'))
        line_buffer=""
        # print(threadno,ct)
        t=False
        while True:
            # line_number = client_socket.recv(1024).decode()
            try:
                line_number = client_socket.recv(1024).decode()
            except ConnectionResetError:
                print(f"Client {threadno} disconnected. Reconnecting...")
                time.sleep(0.00001)
                client_socket, addr = myserver_socket.accept()
                Clients_list[threadno-1] = [client_socket, addr]
                print(f"Reconnected to client {threadno}")
                t=True
                break

            line_buffer +=line_number
            if line_number.endswith("\n"):
                break
        if t :
            continue
        lines=line_buffer.split('\n',1)
        line_number=int(lines[0])
        if line_number==-1: 
            continue 
        line_content=lines[1]
        # print(line_buffer," -> ",threadno)
        if(All_lines[line_number]=="-69"):
            lt+=1
            All_lines[line_number]=line_content
            ct-=1
    # print("out of client ",threadno)
    print(threadno,lt)
    client_socket.close()
    check[threadno]=1

def HandleSir(sirserver_socket):
    global ct
    l=0
    while ct>0:
        line = send_sendline_request(sirserver_socket).split('\n',1)
        x=int(line[0])
        if(x==-1):
            continue
        if All_lines[x]=="-69" : 
            l+=1
            All_lines[x]=line[1]
            ct-=1
        # print("master",ct)
    check[0]=1
    print("expected ",l)
try:
    print("Server started working")
    start_time=time.time()
    while ThreadCount<nclients-1:
        print("hi")
        client_socket,addr=myserver_socket.accept()
        Clients_list.append([client_socket,addr])
        print("Conncted to "+" IP "+addr[0]+" Port : "+str(addr[1]))
        ThreadCount+=1
        start_new_thread(client_thread,(client_socket,ThreadCount,))
        print("Total Thread Count ",ThreadCount)
    print("no of thread : ",ThreadCount+1)
    HandleSir(sirserver_socket)
    while True:
        if check[0]==1:
            submit()
            break
    end_time=time.time()
    print(" total time : ",end_time-start_time)
    while True:
        ok=True
        for i in check:
            if(i==0):
                ok=False
        if(ok):
            break
    
except KeyboardInterrupt:
    print("Server closed by the user")
sirserver_socket.close()