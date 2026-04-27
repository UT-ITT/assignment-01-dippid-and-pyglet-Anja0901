import socket
import time
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = {
    "accelerometer": {
        "x": 0.1,
        "y": 0.2,
        "z": 0.3
    },
    "button_1": False
}


button_state = False
press_end_time = 0

while True:
    t = time.time()

    # Accelerometer
    data["accelerometer"]["x"] = np.sin(t)
    data["accelerometer"]["y"] = np.sin(2*t)
    data["accelerometer"]["z"] = np.sin(3*t+2)

    

    # Button logic
    if button_state and (t > press_end_time):
        button_state = False

    if not button_state:
        if np.random.rand() < 0.02:
            button_state = True
            press_end_time = t + np.random.uniform(0.2, 1.5)  # Button pressed for between 0.2 and 1.5 seconds
    
    data["button_1"] = button_state
   
    # send
    message = str(data).encode()
    print(message)

    sock.sendto(message, (IP, PORT))

    time.sleep(0.05)