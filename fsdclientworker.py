import socket as s
import select
import csv
import os.path
import re
from threading import Event
from sim_data import SimData
from unrealtcpserver import broadcast_json_data

# Global dictionary to store aircraft data
aircraft_list = {}

# Global state to store the latest sim_time we are collecting data for
latest_sim_time = 0

def create_socket_and_connect(server_address):
    connection = s.create_connection(server_address, timeout=5)
    return connection

def process_received_data(buffer):
    global aircraft_list, latest_sim_time
    json_data_list = []
    pattern = rb'SIMDATA:([a-zA-Z0-9]+):([a-zA-Z0-9]+):([a-zA-Z0-9]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9.]+):([-0-9]+):([-0-9]+):([-0-9]+):([-0-9.]+):([-0-9.]+)\r\n'

    # for sebugging
    # Write received data to CSV file
    with open("SimData.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        # Check if file is empty, if so, write header
        if os.path.getsize("SimData.csv") == 0:
            writer.writerow(["Received Data"])
        # Write received data as a single row
        writer.writerow([buffer])
        
    while True:
        match = re.search(pattern, buffer)
        if not match:
            break

        matched_data = match.group(0)
        # Check if the matched data ends with '\r\n'
        if not matched_data.endswith(b'\r\n'):
            break  # Incomplete data, wait for the next chunk
        
        buffer = buffer[match.end():]

        try:
            call_sign, aircraft_type, liveries, sim_time, latitude, longitude, current_altitude, \
            heading, roll, pitch, ground_speed, is_on_the_ground, ils_in_range, maneuver, emergency_flag, \
            airport_altitude, lamp_flag = match.groups()

            # Decode the byte strings
            call_sign = call_sign.decode()
            aircraft_type = aircraft_type.decode()
            liveries = liveries.decode()
            sim_time = sim_time.decode()
            latitude = latitude.decode()
            longitude = longitude.decode()
            current_altitude = current_altitude.decode()
            heading = heading.decode()
            roll = roll.decode()
            pitch = pitch.decode()
            ground_speed = ground_speed.decode()
            is_on_the_ground = is_on_the_ground.decode()
            ils_in_range = ils_in_range.decode()
            maneuver = maneuver.decode()
            emergency_flag = emergency_flag.decode()
            airport_altitude = airport_altitude.decode()
            lamp_flag = lamp_flag.decode()

            # Check if a SimData instance with the call_sign already exists
            if call_sign in SimData._instances:
                # Update existing SimData instance
                sim_data = SimData._instances[call_sign]
                sim_data.update(aircraft_type, liveries, sim_time, latitude, longitude, current_altitude,
                                heading, roll, pitch, ground_speed, is_on_the_ground, ils_in_range, maneuver,
                                emergency_flag, airport_altitude, lamp_flag)
            else:
                # Create a new SimData instance
                sim_data = SimData(call_sign, aircraft_type, liveries, sim_time, latitude, longitude, current_altitude,
                                   heading, roll, pitch, ground_speed, is_on_the_ground, ils_in_range, maneuver,
                                   emergency_flag, airport_altitude, lamp_flag)

            # Update the global aircraft_list
            aircraft_list[call_sign] = sim_data.to_dict()
            # json_data_list.append(sim_data.to_dict())
            json_data_list = list(aircraft_list.values())
            
            # for sebugging
            # print("Dict parsing data:", aircraft_list)
            

        except Exception as e:
            print("Error parsing data:", e)
        
    return buffer, json_data_list

def start_fsd_client(exit_event):
    global latest_sim_time
    server_address = ('127.0.0.1', 6811)
    print('Connecting to FSD Server at', server_address)

    message = "#AAUNREAL:SERVER:Unreal:00000:22222:1:100\r\n$CQUNREAL:@94835:SIMDATA:1"
    buffer = b''
    
    messageMetar = "$AXUNREAL:SERVER:METAR:WIHH"

    while not exit_event.is_set():
        try:
            with create_socket_and_connect(server_address) as connection:
                print('Connected to FSD Server')
                connection.sendall(str.encode(message))

                while not exit_event.is_set():
                    ready = select.select([connection], [], [], 5)
                    if ready[0]:
                        received_data = connection.recv(1024)
                        if received_data.startswith(b'#TMserver:'):
                            connection.sendall(str.encode(message))
                            print("Received data from Euroscope:", received_data)

                        buffer += received_data
                        # buffer, json_data_list = process_received_data(buffer)

                        # # for json_data in json_data_list:
                            # # broadcast_json_data(json_data)

                        # broadcast_json_data(json_data_list)
                        
                        #broadcast when buffer end (not working)
                        if buffer.endswith(b'\r\n'):
                            buffer, json_data_list = process_received_data(buffer)

                            broadcast_json_data(json_data_list)
                            
                            # connection.sendall(str.encode(messageMetar))

                        # while b'\r\n' in buffer:
                            # buffer, json_data_list = process_received_data(buffer)                        
                            
                            # # Broadcast only when we have data with the same sim_time
                            # if len(aircraft_list) > 0:
                                # matching_time_data = [
                                    # data for data in aircraft_list.values() if data["sim_time"] == latest_sim_time
                                # ]
                                # if len(matching_time_data) == len(aircraft_list):
                                    # broadcast_json_data(json_data_list)
                                    
                                    # # Reset latest_sim_time only if new sim_time is larger
                                    # next_sim_time = max(data["sim_time"] for data in matching_time_data)
                                    # if next_sim_time > latest_sim_time:
                                        # latest_sim_time = next_sim_time
                                    # aircraft_list.clear()

                    else:
                        print("No response received within 5 seconds. Please connect Euroscope to FSD server!")
                        connection.sendall(str.encode(message))

        except s.timeout:
            print("Connection attempt timed out. The FSD server may not be active.")
        except ConnectionResetError:
            print("The connection was reset. Restart to continue.")
        except ConnectionAbortedError:
            print("The connection closed. Restart to continue.")
        except ConnectionRefusedError:
            print("The connection was refused. Please check FSD server is open.")
        except OSError as e:
            print(f"An OS error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# if __name__ == "__main__":
    # exit_event = Event()
    # start_fsd_client(exit_event)
