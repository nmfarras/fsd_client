# # main.py

# import threading
# import time
# import unrealtcpserver
# import fsdclientworker

# if __name__ == "__main__":
    # # Start TCP server in a separate thread
    # server_thread = threading.Thread(target=unrealtcpserver.start_tcp_server)
    # server_thread.start()

    # # Start FSD client connection in a separate thread
    # client_thread = threading.Thread(target=fsdclientworker.start_fsd_client)
    # client_thread.start()

    # # Keep the main thread running
    # while True:
        # time.sleep(1)

# main.py

import threading
import time
import unrealtcpserver
import fsdclientworker

# Event to signal termination
exit_event = threading.Event()

if __name__ == "__main__":
    # Start TCP server in a separate thread
    server_thread = threading.Thread(target=unrealtcpserver.start_tcp_server, args=(exit_event,))
    server_thread.start()

    # Start FSD client connection in a separate thread
    client_thread = threading.Thread(target=fsdclientworker.start_fsd_client, args=(exit_event,))
    client_thread.start()

    # Wait for termination signal
    try:
        while not exit_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Terminating...")
        exit_event.set()  # Set the exit event to terminate threads

        # Wait for threads to complete before exiting
        server_thread.join()
        client_thread.join()

    print("Exiting program.")