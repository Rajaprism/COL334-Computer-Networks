import socket
import hashlib
import time

# Server details
server_host = "10.17.7.218"
server_host="127.0.0.1"
server_port = 9801
start=time.time()

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the timeout for receiving a response (in seconds)
timeout = 0.1

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

# Define the maximum number of bytes per request
max_bytes_per_request = 1448


def SendRequest(offset,cwnd,ai_factor,mi_factor):

    print(offset,"--------------------------------------------",cwnd)
    count=0
    for i in range(cwnd):
        num_to_receive=min(max_bytes_per_request,num_bytes-(offset+i*max_bytes_per_request))
        if(num_to_receive==0):
            break

        count+=1
        offset_request = f"Offset: {offset+i*max_bytes_per_request}\nNumBytes: {num_to_receive}\n\n"
        udp_socket.sendto(offset_request.encode(), (server_host, server_port))

    udp_socket.settimeout(timeout)
    responses=[]

    while True:
        if(count==0):
            cwnd+=1
            break
        try:
            response, _ = udp_socket.recvfrom(4096)
            response = response.decode()

            if response.startswith("Offset: "):
                count-=1
                responses.append(response)

        except socket.timeout:
            print("Timeout: No response received within the timeout period.")
            cwnd=int(cwnd*mi_factor)
            break

    
    my_offset=[]
    for offset_response in responses:

        received_offset = int(offset_response.split("\n")[0].split(": ")[1])
        received_num_bytes = int(offset_response.split("\nNumBytes: ")[1].split("\n")[0])
        received_data = offset_response.split("\n\n", 1)[1].encode()

        my_offset.append(received_offset)
        data_buffer[received_offset // 1448] = (received_offset, received_num_bytes, received_data)

    my_offset.sort(reverse=True)


    while len(my_offset)!=0:
        num_to_receive=min(max_bytes_per_request,num_bytes-offset)

        if(num_to_receive==0):
            break

        if(offset==my_offset[-1]):
            offset=my_offset[-1]+num_to_receive
            my_offset.pop()
        else:
            break

    return [offset,cwnd]


def RunAIMD():
    # Request and receive data in chunks
    mincwnd=1
    cwnd=1
    ai_factor=1
    mi_factor=0.5
    offset=0
    while offset<num_bytes:
        response=SendRequest(offset,cwnd,ai_factor,mi_factor)
        # print("init ",offset," final ",response[0]," initcwnd ",cwnd," finalcwnd ",response[1])
        offset=response[0]
        cwnd=max(mincwnd,response[1])



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


