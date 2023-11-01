from socket import *
import hashlib
import time
import csv
# squish_timestamps = []
# burst_sizes=[]
# sequence_numbers = []
data_log = []
offset_log = []
begin= time.time()
serverName = '127.0.0.1'
serverPort = 9802
clientSocket = socket(AF_INET, SOCK_DGRAM)
numByt = 1448
request1 = 'SendSize\n\Reset\n\n'
INITIAL_TIMEOUT = 0.01

# Dynamic Timeout parameters
avg_rtt = INITIAL_TIMEOUT  # Initial average RTT (in seconds)
ALPHA = 0.25  # Weight for the EMA
MARGIN = 5 # Margin factor
BETA = 0.25
dev_rtt = 0.0
flag = 0
# AIMD parameters
base_burst_size = 1  # initial size of the burst
burst_size = base_burst_size
alpha = 1  # amount to increase during additive increase
beta = 0.4  # fraction to decrease during multiplicative decrease

data = ['']
#local server ---- flag = 3
def send_burst(offsets):
    global flag
    for offset in offsets:
        if offset == totalpackets-1:
            request = 'Offset: '+ str(1448*offset) + '\nNumBytes: ' + str(last_pack) + '\n\n'
        else:
            request = 'Offset: '+ str(1448*offset) + '\nNumBytes: ' + str(numByt) + '\n\n'
        clientSocket.sendto(request.encode(), (serverName, serverPort))
        offset_log.append((time.time()-begin, 1448*offset, 'request'))
        # time.sleep(0.1**20)
        if(flag==2):
            time.sleep(0.000001)
            flag = 0
        flag += 1
        

totalSize = 0
while True:
    try:
        clientSocket.sendto(request1.encode(), (serverName, serverPort))
        clientSocket.settimeout(avg_rtt + MARGIN * dev_rtt)  # set the timeout based on avg_rtt and margin
        response1, serverAddress = clientSocket.recvfrom(2048)
        totalSize = int(response1.decode().split(' ')[1])
        break
    except timeout:
        print(f"No response received, resending the request... Current Average RTT: {avg_rtt:.3f}s")

totalpackets = totalSize // 1448 + (1 if totalSize % 1448 != 0 else 0)
last_pack = totalSize % 1448
data = [''] * totalpackets
pending_packets = set(range(totalpackets))

while pending_packets:
    current_burst = list(pending_packets)[:burst_size]

    send_burst(current_burst)

    start_time = time.time()
    try:
        for _ in range(burst_size):
            # print(avg_rtt,dev_rtt)
            clientSocket.settimeout(avg_rtt + MARGIN * dev_rtt)
            response, serverAddress = clientSocket.recvfrom(2048)

            rtt = time.time() - start_time  # Calculate the RTT for the received packet
            avg_rtt = (1 - ALPHA) * avg_rtt + ALPHA * rtt  # Update the EMA of the RTT
            dev_rtt = (1-BETA)*dev_rtt + BETA*abs(rtt-avg_rtt)
            dec_res = response.decode()
            if dec_res.startswith("Offset"):
                offset, numBytes, waste, pdata = dec_res.split('\n', 3)
                if waste == "Squished":
                    # squish_timestamps.append(time.time())
                    pdata = pdata.split("\n", 1)[1]

                offset_value = int(offset.split(' ')[1])
                offset_log.append((time.time()-begin, offset_value, 'reply'))
                print("bytes recv -------------------- offset: " + str(offset) + " numBytes: "+ str(numBytes))

                if data[offset_value // 1448] == '':
                    data[offset_value // 1448] = pdata
                    # sequence_numbers.append((time.time(), offset_value))
                    current_time = time.time()-begin
                    data_log.append((current_time, burst_size, waste == "Squished"))
                    pending_packets.remove(offset_value // 1448)

        # Additive Increase
        burst_size += alpha
        # burst_sizes.append((time.time(), burst_size))
        print("new burst size is , ",burst_size)

    except timeout:
        # print(f"Timeout! Reducing burst size to {burst_size}. Current Average RTT: {avg_rtt:.3f}s")
        # Multiplicative Decrease
        burst_size = max(base_burst_size, int(burst_size * beta))
        # burst_sizes.append((time.time(), burst_size))
        print("new burst size is , ",burst_size)

combined_data = ''.join(data)
m = hashlib.md5()
m.update(combined_data.encode())
md5_hash = m.hexdigest()
request3 = "Submit: 2021CS10578@col334\nMD5: "+str(md5_hash)+"\n\n"
while True:
    clientSocket.sendto(request3.encode(), (serverName, serverPort))
    try:
        submit_response, serverAddress = clientSocket.recvfrom(2048)
        while submit_response.decode().split(":", 2)[0] != "Result":
            submit_response, serverAddress = clientSocket.recvfrom(2048)    
        res = submit_response.decode()
        print(res)
        # print(time.time()*1000 - begin)
        break
    except:
        pass



with open("data_log.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Burst Size", "Squished"])  # Write header
    writer.writerows(data_log)

with open("offset_log.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Offset", "Type"])  # Write header
    writer.writerows(offset_log)

