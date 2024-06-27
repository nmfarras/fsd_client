# unrealtcpserver.py

import socket as s
import threading
import json

# Lock for thread safety
client_connections_lock = threading.Lock()

# Class to represent client connections
class ClientConnection:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        self.client_name = None
        self.unique_id = None
        self.status = 'active'  # Initial status is active

    def set_client_name(self, name):
        self.client_name = name

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id

    def set_status_inactive(self):
        self.status = 'inactive'

    def close(self):
        self.client_socket.close()

# Global variable to store client connections
client_connections = {}

# Function to handle connections from clients
def handle_client_connection(client_socket, client_address):
    client_connection = ClientConnection(client_socket, client_address)
    client_connection.set_unique_id(hash(client_socket))
    
    with client_connections_lock:
        client_connections[client_connection.unique_id] = client_connection

    while True:
        request = client_socket.recv(1024)
        if not request:
            break
        # Handle client request here
        # For now, let's just echo back the received data
        client_socket.send(request)

    # Client disconnected, set status to 'inactive'
    client_connection.set_status_inactive()

    # Close client socket
    client_connection.close()
    
    with client_connections_lock:
        del client_connections[client_connection.unique_id]

# Function to broadcast JSON data to all connected clients
def broadcast_json_data(json_data_list):
    # Encapsulate JSON data inside 'data' property
    
    json_to_send = {'data':{'aircraft_positions':[]}}
    
    # json_to_send['data']['aircraft_positions'].append(json_data_list)
    
    for json_data in json_data_list:
        json_to_send['data']['aircraft_positions'].append(json_data)
    
    # for sebugging
    # print("Constructed JSON data:", json.dumps(json_to_send))
    
    with client_connections_lock:
        for connection_id, connection in client_connections.items():
            try:
                connection.client_socket.sendall(json.dumps(json_to_send).encode())
            except Exception as e:
                print(f"Error broadcasting data to {connection.client_address}: {e}")

# Function to start TCP server
def start_tcp_server(exit_event):
    server_address = ('127.0.0.1', 9999)
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    try:
        server.bind(server_address)
        server.listen(5)  # Listen for incoming connections
        print('TCP Server listening on', server_address)

        while not exit_event.is_set():
            client_socket, client_address = server.accept()
            print('Accepted connection from', client_address)
            client_handler = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
            client_handler.start()

    except OSError as e:
        print(f"Error: Failed to bind the server to {server_address}: {e}")
    
    finally:
        # Close all client sockets
        with client_connections_lock:
            for connection_id, connection in client_connections.items():
                connection.close()

        # Close the server socket
        server.close()
