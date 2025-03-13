import socket
import sys
import threading
import time

# Add Freenove libraries
sys.path.append('/home/pi/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server')

from motor import Ordinary_Car
from ultrasonic import Ultrasonic

# Initialize motor and ultrasonic modules
car = Ordinary_Car()
ultrasonic = Ultrasonic()

# Server configuration
HOST = "10.0.0.65" 
PORT = 65432  # port number
clients = []  # List clients

current_direction = "Stopped"

def handle_client(client_socket):
    """Handles communication with client."""
    global current_direction  

    try:
        while True:
            # Receive data
            data = client_socket.recv(1024).decode().strip()
            print(f"Raw data received: {repr(data)}")  # Debugging 

            if not data:
                break

            if data in ['forward', 'backward', 'left', 'right', 'stop', 'distance', 'exit']:
                print(f"Received command: {data}")
                
            power_val = 1000  # Initial motor value

            # Process commands
            if data == 'forward' or data == 'backward' or data == 'left' or data == 'right':
                if data == 'forward':
                    car.set_motor_model(power_val, power_val, power_val, power_val)
                    current_direction = "Moving Forward"
                elif data == 'backward':
                    car.set_motor_model(-power_val, -power_val, -power_val, -power_val)
                    current_direction = "Moving Backward"
                elif data == 'left':
                    car.set_motor_model(-power_val, -power_val, power_val, power_val)
                    current_direction = "Turning Left"
                elif data == 'right':
                    car.set_motor_model(power_val, power_val, -power_val, -power_val)
                    current_direction = "Turning Right"
                    
                # Send direction update to client
                client_socket.sendall(f"Direction: {current_direction}\n".encode())

            elif data == 'stop':
                car.set_motor_model(0, 0, 0, 0)
                current_direction = "Stopped"
                # Send direction update to the client
                client_socket.sendall(f"Direction: {current_direction}\n".encode())

            elif data == 'distance':
                try:
                    # Get distance from the ultrasonic 
                    distance = ultrasonic.get_distance()
                    
                    if distance is not None:
                        client_socket.sendall(f"Distance: {distance:.2f} cm\n".encode())  # Send distance to client
                    else:
                        client_socket.sendall("Error: Could not read distance\n".encode())  # Error message
                except Exception as e:
                    client_socket.sendall(f"Error reading distance: {e}\n".encode())

            elif data == 'exit':
                client_socket.sendall("Closing connection\n".encode())
                break
            else:
                client_socket.sendall("Invalid command\n".encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    """Starts the Wi-Fi server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
