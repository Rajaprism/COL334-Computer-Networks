import socket
import hashlib
import time

# Server details
# server_host = "10.17.6.5"
server_host="127.0.0.1"
server_port = 9801
# java UDPServer 9801 big.txt 10000 constantrate notournament verbose

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the timeout for receiving a response (in seconds)
timeout = 0.02

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

# Define the maximum number of bytes per request
max_bytes_per_request = 1448
alpha=0.2
beta=0.5


def SendRequest(cwnd,mi_factor,EstimatedRTT,DevRTT,TimeOut):
    print("Time Out : ",TimeOut," windowsize : ",cwnd)
    requested_offset=set([])
    n=len(All_offset)
    count=min(int(cwnd),n)
    start=time.time()
    for i in range(count):

        num_to_receive=min(max_bytes_per_request,num_bytes-(All_offset[-1]))
        offset_request = f"Offset: {All_offset[-1]}\nNumBytes: {num_to_receive}\n\n"
        udp_socket.sendto(offset_request.encode(), (server_host, server_port))

        requested_offset.add(All_offset[-1])

        All_offset.pop()

    udp_socket.settimeout(TimeOut)
    responses=[]

    while True:
        time.sleep(0.004)
        if(count==0):
            cwnd=cwnd+(1/cwnd)
            break
        try:
            response, _ = udp_socket.recvfrom(4096)
            response = response.decode()

            if response.startswith("Offset: "):
                count-=1
                responses.append(response)
                end=time.time()
                SampleRTT=(end-start)
                start=end
                DevRTT=(1-beta)*DevRTT+beta*abs(SampleRTT-EstimatedRTT)
                EstimatedRTT=(1-alpha)*EstimatedRTT+alpha*SampleRTT
                TimeOut=EstimatedRTT+4*DevRTT
                udp_socket.settimeout(TimeOut)

        except socket.timeout:
            # print(f"Timeout: No response received for request. Retrying...")
            cwnd=cwnd*mi_factor
            break

    for offset_response in responses:

        received_offset = int(offset_response.split("\n")[0].split(": ")[1])
        received_num_bytes = int(offset_response.split("\nNumBytes: ")[1].split("\n")[0])
        received_data = offset_response.split("\n\n", 1)[1].encode()

        requested_offset.discard(received_offset)
        data_buffer[received_offset // 1448] = (received_offset, received_num_bytes, received_data)

    for off in requested_offset:
        All_offset.append(off)


    return [cwnd,EstimatedRTT,DevRTT,TimeOut]


def RunAIMD():
    # Request and receive data in chunks
    cwnd=1.0
    mi_factor=0.5
    EstimatedRTT=0.05
    DevRTT=0.001
    TimeOut=0.01
    for offset in range(0, num_bytes, max_bytes_per_request):
        All_offset.append(offset)

    while len(All_offset):
        response=SendRequest(cwnd,mi_factor,EstimatedRTT,DevRTT,TimeOut)
        cwnd=max(1.0,response[0])
        EstimatedRTT=response[1]
        DevRTT=response[2]
        TimeOut=response[3]
        # print("Printing the current window size : ",cwnd)



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
