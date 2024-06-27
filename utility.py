# utility.py

def send_message(connection, message):
    try:
        connection.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")