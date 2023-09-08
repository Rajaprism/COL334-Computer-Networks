import socket
import threading
import time

# data_lock = threading.Lock()  
# lines_sent_lock = threading.Lock() 
# clients_lock = threading.Lock()


global count
global tt
global index_reached
index_reached = -1
count=0
global flag 
flag = False

lines_in_array = set()
lines_data = [None for i in range(1000)] 
client_thrds = []
# connected_clients = []
lines_sent_to_clients = {("10.194.28.225",55505): set()}
# lines_received_from_clients = {("10.194.28.225",55505): set(), ("10.194.26.65",)}
mapping={"10.194.26.65":"disha","10.194.42.2":"srushti","10.194.14.9":"namrata","10.194.28.225":"aastha"}

def connect_to_server():
    try:
            server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(('10.17.7.134', 9801))
            buffer = ""
            while count != 1000:
                request = "SENDLINE\n"
                server_socket.send(request.encode())
                # print("sending to vayu")
                data = server_socket.recv(1024).decode()
                buffer += data
                while buffer.count('\n') >= 2:
                    line_number_str, line_content, buffer = buffer.split('\n', 2)
                    # print("Line_num is ................", line_number_str)
                    # print("line_content is................", line_content)'
                    if(line_number_str.isdigit()):
                        line_number = int(line_number_str)
                        if (line_number!=-1) and (lines_data[line_number] == None):
                            update_lines_data(line_number,line_content)
                            if count==1000:
                                break
                    # print(f"Line Number: {line_number}, Content: {line_content}")
                if count==1000:
                    et = time.time()
                    print(et-tt)   
                    for x in client_thrds:
                        x.start()
                    flag = True
                    # print("Thread killed")
                    # print("Checking ", client_thrds[0].is_alive())
                    # if not client_thrds[0].is_alive() :
                    submission_message = "SUBMIT\ndisha@col334-672\n1000\n"
                    server_socket.send(submission_message.encode())
                    # print("submit request sent")
                    for i in range(0,1000):
                        msg = str(i)+"\n"
                        server_socket.send(msg.encode())
                        msg2 = lines_data[i]+"\n"
                        server_socket.send(msg2.encode())
                        # print("Line number sent : ", i)
                    res = server_socket.recv(1024).decode().strip()
                    et = time.time()
                    print(et-tt)
                    while(res.startswith("SUBMIT")!=True):
                        # print("*****Not valid response******")
                        res = server_socket.recv(1024).decode().strip()
                    
                    print(res)
                    server_socket.close()
                    et = time.time()
                    print(et-tt,'seconds')

                    break
    except Exception as e:
        print(f"Error in connect_to_server: {e}")

def start_server():
    """Starts the server to listen on the given port."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12344))
    server_socket.listen(5)  # Adjust the backlog as needed
    
    print(f"Server started. Listening for connections on port {12345}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
        # client_thread.start()
        client_thrds.append(client_thread)


def handle_client_connection(conn:socket, addr):
    global count
    global flag
    """Handle individual client connections."""
    while not flag:
        print(f"Accepted connection from {addr}")

        # with clients_lock:
        #     connected_clients.append(conn)  # Add the client to the list of connected clients
        lines_sent_to_clients[conn] = set()

        try:
            i=0
            # while True:
                # while count != 1000:  # Safely iterate over our lines_data
            while i<1000:
                # while i<len(lines_data):
                # print("==========================",i)
                # with lines_sent_lock:  # Safely check and update lines_sent_to_clients
                        # send_message = f"LINE:{index}:{line}"
                send_message = str(i)+"\n"+lines_data[i]+"\n"
                # print("sending==============")
                # print(str(i)+"\n"+lines_data[i]+"\n")
                conn.send(send_message.encode())
                # print("line no. sent: " , i)
                # print("sent successfullly")
                # lines_sent_to_clients[conn].add(lines_data[i][0])
                i+=1
            
        except Exception as e:  
            print(f"Error handling client {addr}: {e}")
        finally:
            # with clients_lock:
                # connected_clients.remove(conn)  # Remove the client from the list of connected clients
            # print("above close")
            conn.close()
            flag = True
            # print("flag is ",True)

def update_lines_data(line_number, line_content):
    global count
    # with data_lock:
    lines_data[line_number] = line_content
    count += 1
    # print("Count is ", count)

def client_handler(client_address):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # print("before")
            client_socket.connect(client_address)
            # print("req sent")
            buffer = ""
            while True:
                # Listen for data from the client
                
                message = client_socket.recv(1024).decode()
                # print(message)
                # if(len(message)>0):
                    # print("received from someone --------------------------------")
                    # print("recieved from ",mapping[client_address[0]])
                if message == "DONE":
                    print("-----------------------------------------------------------------------------------------------")
                    break
                else:
                    buffer += message
                    while buffer.count('\n') >= 2:
                        line_number_str, line_content, buffer = buffer.split('\n', 2)
                        # print("Line_num is ................", line_number_str)
                        # print("line_content is................", line_content)
                        if(line_number_str.isdigit()):
                            line_number = int(line_number_str)
                            if (line_number!=-1) and (lines_data[line_number] == None):
                                # print("recieved from ",mapping[client_address[0]])
                                update_lines_data(line_number,line_content)
                                if count==1000:
                                    break
                if count==1000:
                    client_socket.send("DONE".encode())
                    # client_socket.close()
                    break
                # else:
                    # client_socket.send("CONTINUE".encode())

    except Exception as e:
        print(f"Error in client_handler ({client_address}): {e}")
def main():
    # Threads list to keep track of all threads
    global tt
    tt = time.time()
    threads = []
    other_clients = [("10.194.2.66",55555),("10.194.28.225",55505),("10.194.42.2",55507)]
    # ,('10.194.42.129', 55503)
    for client_address in other_clients:
        client_thread = threading.Thread(target=client_handler, args=(client_address,))  
        threads.append(client_thread)
        client_thread.start()

    listener_thread = threading.Thread(target=start_server)
    threads.append(listener_thread)
    listener_thread.start()
    # Connect to vayu.iitd.ac.in
    server_thread = threading.Thread(target=connect_to_server)
    threads.append(server_thread)
    # print("before start")
    server_thread.start()
    print("after start")
    

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    print("All threads completed!")
    et=time.time()
    print(et-tt,'seconds')

# Start the program
if __name__ == "__main__":
    main()