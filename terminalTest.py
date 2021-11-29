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
        
def main():
    blue_comm = BluetoothComm()
    buff_msg = b''
    while True:
        get = blue_comm.read_comm()
        blue_comm.send_comm("hello")
        command = get.decode("utf-8")
        print(command[-1] == '\r')
        print(command[-1] == '\n')
        print(get)
        print(command.encode("utf-8"))

        if command[-1] != '\r':
            print("yes")
            buff_msg += get
        else:
            print("no")
            buff_msg += command[:-1].encode("utf-8")
            print(buff_msg)
            p = subprocess.Popen([b'bash',b'-c',buff_msg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            shell_out = p.communicate()
            print('shell:',shell_out)
            blue_comm.send_comm('\n')
            if shell_out[0] != b'':
                blue_comm.send_comm(shell_out[0])
            else:
                blue_comm.send_comm(shell_out[1])
            blue_comm.send_comm('\r')
            buff_msg = b''
main()
