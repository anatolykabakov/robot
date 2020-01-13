import serial
import time

#Arduino protocol
set_command = 'v'
print_command = 'd'
start_connect = 's'

class protocol():
    def __init__(self, port, rate):
        self.connect = self.openconnect(port, rate)

    def check_connect(self, connect):
        c = connect.read(1).decode()
        if c != 'c':
            self.stop()

    def openconnect(self, port, rate):
        connect = serial.Serial(port, rate)
        time.sleep(1)
        while not connect.is_open:
            self.openconnect(port, rate)
        is_connected = False
        while not is_connected:
            print("Waiting for arduino...")
            connect.write(start_connect.encode())
            connect_flag = connect.read(1).decode()
            self.check_connect(connect)
            if not connect_flag:
                time.sleep(0.1)
                continue
            if connect_flag == 'r':
                is_connected = True
                print('Connected!')
        return connect

    def arduino_stop(self):
        self.setMotors(0,0)
        self.connect.close()

    def stop(self):
        self.arduino_stop()

    def getMotors(self):
        self.connect.write(print_command.encode())
        data = self.connect.read(30).decode()
        #print(data) 
        self.check_connect(self.connect)
        data = data.split(';')
        x = float(data[0])
        y = float(data[1])
        yaw = float(data[2])
        v = float(data[3])
        w = float(data[4])
        return x, y, yaw, v, w
 
    def setMotors(self, v, w):
        self.send(v, w)

    def send(self, lvel, avel):
        ### TODO: round(x, 2) or round(x, 1)
        send_data = set_command + str(round(lvel,2)) + ' ' + str(round(avel,2)) + "\n"
        self.connect.write(send_data.encode())
        self.check_connect(self.connect)
    