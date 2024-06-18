# server.py

import socket
import threading

# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    # Loop to handle incoming messages from the client
    while True:
        # Receive message from the client
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        
        print(f"[{client_address}] {message}")

        # Broadcast the received message to all other clients
        broadcast(message, client_socket)

    # When client disconnects
    print(f"[DISCONNECTED] {client_address}")
    client_socket.close()

# Function to broadcast message to all clients except the sender
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If sending message fails (client disconnected), remove the client
                clients.remove(client)

# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))  # Change 'localhost' to your IP address if needed
server.listen()

print("[SERVER] Waiting for connections...")

clients = []

# Main loop to accept incoming connections
while True:
    client_socket, client_address = server.accept()
    clients.append(client_socket)

    # Start a new thread to handle client connection
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()

