import socket
import hashlib
import time
from _thread import *
# Server details
server_host = "10.17.7.218"
# server_host = "127.0.0.1"
server_port = 9802
start=time.time()

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the TimeOut for receiving a response (in seconds)
timeout = 0.01

def send_and_receive(request, expected_response_prefix):

    while True:
        udp_socket.sendto(request.encode(), (server_host, server_port))
        udp_socket.settimeout(timeout)
        try:
            response, _ = udp_socket.recvfrom(4096)
            response = response.decode()

            if response.startswith(expected_response_prefix):
                return response
            
        except socket.timeout:
            print(f"Timeout: No response received for request. Retrying...")
    
def findSize():
    request="SendSize\nReset\n\n"
    expected_response_prefix="Size: "
    response=send_and_receive(request,expected_response_prefix)
    return int(response.split(": ")[1])


# the number of bytes to receive
num_bytes = findSize()
print("Total size to be received : ",num_bytes)

# Create a buffer to store received data
data_buffer = [None] * (num_bytes // 1448 + 1)

All_offset=[]
offset=[]

# Define the maximum number of bytes per request
max_bytes_per_request = 1448

check=True

squished_no=0
# sleep time for sendrequest is 0.007 fine
def SendRequest(threadno):
    global check
    global All_offset
    print("Thread No hi bye noentry : ",threadno)
    c=0
    while(len(All_offset)!=0):
        time.sleep(0.008)
        num_to_receive=min(max_bytes_per_request,num_bytes-(All_offset[-1]))
        offset_request = f"Offset: {All_offset[-1]}\nNumBytes: {num_to_receive}\n\n"
        udp_socket.sendto(offset_request.encode(), (server_host, server_port))
        All_offset.pop()
        c+=1
    check=False

def ReceiveRequest():
    global offset
    global squished_no
    while(len(offset)!=0):
        try:
            response, _ = udp_socket.recvfrom(4096)
            response = response.decode()

            if response.startswith("Offset: "):
                received_offset = int(response.split("\n")[0].split(": ")[1])
                received_num_bytes = int(response.split("\nNumBytes: ")[1].split("\n")[0])
                received_data = response.split("\n\n", 1)[1].encode()

                print("received_offset : ",received_offset)
                
                if(data_buffer[received_offset // 1448]==None):
                    offset.remove(received_offset)
                    data_buffer[received_offset // 1448] = (received_offset, received_num_bytes, received_data)
            if "Squished" in response:
                squished_no+=1
        except socket.timeout:
            print(f"Timeout: No response received for request. Retrying...")

def RunAIMD():
    global All_offset
    global check
    for i in range(0, num_bytes, max_bytes_per_request):
        All_offset.append(i)
        offset.append(i)
    start_new_thread(ReceiveRequest,())
    threadno=1
    while len(All_offset)!=0:
        check=True
        SendRequest(threadno)
        All_offset=offset[:]
    


def CheckResult():
    # Assemble the data in the correct order
    assembled_data = bytearray(num_bytes)

    for data in data_buffer:
        if(data is None):
            print("Data is None")
            continue
        assembled_data[data[0]:data[0]+data[1]] = data[2]

    # Calculate MD5 hash of the received data
    md5_hash = hashlib.md5(assembled_data).hexdigest()

    # Submit the MD5 hash to the server
    submit_request = f"Submit: [1@nothing]\nMD5: {md5_hash}\n\n"

    # Receive the Result response
    result_response = send_and_receive(submit_request, "Result: ")

    # Parse the Result response
    if result_response.startswith("Result: "):

        result = result_response.split("\n")[0].split(": ")[1].strip()
        time_taken = float(result_response.split("\nTime: ")[1].split("\n")[0])
        penalty = float(result_response.split("\nPenalty: ")[1].split("\n")[0])

        print(f"Result: {result}")
        print(f"Time taken (ms): {time_taken}")
        print(f"Penalty: {penalty}")
        
    else:

        print("Error: Failed to get the result from the server.")

    udp_socket.close()


RunAIMD()
CheckResult()

print("NO of time squished : ",squished_no)