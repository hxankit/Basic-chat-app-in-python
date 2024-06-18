# client.py

import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # If receiving message fails (server disconnected), exit
            print("[ERROR] Connection to server lost.")
            client_socket.close()
            break

# Setup client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))  # Change 'localhost' to server's IP address if needed

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

# Main loop to send messages to the server
while True:
    message = input()
    client.send(message.encode('utf-8'))

# Close the client socket when done
client.close()
