import bluetooth
import subprocess

class BluetoothComm:
    def __init__(self):
        self.server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        self.server_socket.bind(("",port))
        self.server_socket.listen(1)
        self.client_socket,address = self.server_socket.accept()
        print("Accepted connection from ",address)
        
    def read_comm(self):
        res = self.client_socket.recv(1024)
        if len(res):
            return res
        else:
            return None
 
    def send_comm(self, text):
        self.client_socket.send(text)