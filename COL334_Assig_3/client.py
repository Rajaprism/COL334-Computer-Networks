import socket
import hashlib
import time

server_ip="127.0.0.1"
server_port = 9801
buffer_size = 1024  # Adjust as needed

def send_request(socket, request):
    print("sending request...")
    socket.sendto(request.encode(), (server_ip, server_port))

def receive_response(socket, buffer_size):
    print("receiving the response...")
    data,server_address = socket.recvfrom(buffer_size)
    return data

def submit_data(client_socket,assembled_data):

    md5_hash = hashlib.md5(assembled_data).hexdigest()
    submit_request = f"Submit: 2021CS10915@team\nMD5: {md5_hash}\n\n"
    send_request(client_socket, submit_request)

    verification_response = receive_response(client_socket, buffer_size)


def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Step 1: Send "SendSize" Request
    send_request(client_socket, "SendSize\n\n")

    # Step 2: Receive and Process Size Response
    size_response = receive_response(client_socket, buffer_size)
    size = int(size_response.decode().split(":")[1].strip())

    print("Maximum Limit to Data : ", size)

    # Step 5: Send Requests for Data
    offset = 0
    num_bytes = 1448 # Maximum number of bytes per request
    assembled_data = b''  # Initialize as bytes

    while offset < size:

        request = f"Offset: {offset}\nNumBytes: {num_bytes}\n\n"
        send_request(client_socket, request)

        # Step 6: Receive and Assemble Data
        data_response = receive_response(client_socket, buffer_size)

        data=data_response.decode().split("\n")
        print("..........")
        print(data[0])
        print(data[1])
        print(data[2:])
        assembled_data += data_response
        offset += len(data_response)
        time.sleep(1)

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()
