from socket import *
import hashlib
import time
import logging


# logging.basicConfig(filename='client_log.txt', level=logging.INFO, format='%(message)s')
start_time = time.time()*1000
serverName = "10.17.7.218"
serverPort = 9801
clientSocket = socket(AF_INET, SOCK_DGRAM)
numByt = 1448
request1 = 'SendSize\n\Reset\n\n'
TIMEOUT = 0.05

# AIMD parameters
base_burst_size = 1  # initial size of the burst
burst_size = base_burst_size
alpha = 1  # amount to increase during additive increase
beta = 0.7  # fraction to decrease during multiplicative decrease

data = ['']

def send_burst(offsets):
    for offset in offsets:
        if offset == totalpackets-1:
            request = 'Offset: '+ str(1448*offset) + '\nNumBytes: ' + str(last_pack) + '\n\n'
        else:
            request = 'Offset: '+ str(1448*offset) + '\nNumBytes: ' + str(numByt) + '\n\n'
        clientSocket.sendto(request.encode(), (serverName, serverPort))
        # timestamp = time.time() * 1000 - start_time
        # logging.info(f"RequestSent, Offset: {1448*offset}, Time: {timestamp}")

totalSize = 0
while True:
    try:
        clientSocket.sendto(request1.encode(), (serverName, serverPort))
        clientSocket.settimeout(TIMEOUT)
        response1, serverAddress = clientSocket.recvfrom(2048)
        totalSize = int(response1.decode().split(' ')[1])
        break
    except timeout:
        print("No response received, resending the request...")

totalpackets = totalSize // 1448 + (1 if totalSize % 1448 != 0 else 0)
last_pack = totalSize % 1448
data = [''] * totalpackets
pending_packets = set(range(totalpackets))

while pending_packets:
    current_burst = list(pending_packets)[:burst_size]

    send_burst(current_burst)
    
    try:
        for _ in range(burst_size):
            response, serverAddress = clientSocket.recvfrom(2048)
            timestamp = time.time() * 1000 - start_time

            dec_res = response.decode()
            # offset_value = int(dec_res.split(' ')[1].split(":")[1])
            # logging.info(f"ReplyReceived, Offset: {offset_value}, Time: {timestamp}")
            offset, numBytes, waste, pdata = dec_res.split('\n', 3)
            if waste == "Squished":
                pdata = pdata.split("\n",1)[1]
            # is_squished = "Yes" if "Squished" in waste else "No"

            offset_value = int(offset.split(' ')[1])
            # logging.info(f"ReplyReceived, Offset: {offset_value}, Time: {timestamp}, Squished: {is_squished}")
            # print("bytes recv -------------------- offset: " + str(offset) + " numBytes: "+ str(numBytes))
            if data[offset_value // 1448]=='':
                data[offset_value // 1448] = pdata
                pending_packets.remove(offset_value // 1448)

        # Additive Increase
        burst_size += alpha
        # print("new burst size is , ",burst_size)

    except timeout:
        # Multiplicative Decrease
        burst_size = max(base_burst_size, int(burst_size * beta))
        # print(f"Timeout! Reducing burst size to {burst_size}...")

combined_data = ''.join(data)
m = hashlib.md5()
m.update(combined_data.encode())
md5_hash = m.hexdigest()
request3 = "Submit: 2021CS10578@col334\nMD5: "+str(md5_hash)+"\n\n"
clientSocket.sendto(request3.encode(), (serverName, serverPort))
submit_response, serverAddress = clientSocket.recvfrom(2048)
while submit_response.decode().split(":",2)[0] != "Result":
    submit_response,serverAddress = clientSocket.recvfrom(2048)
res = submit_response.decode()
print(res)    


end_time = time.time()*1000

print(int(end_time-start_time))