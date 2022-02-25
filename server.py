import socket
import sys
import threading
import datetime


class Server:
    def __init__(self):
        self.server_address = ('127.0.0.1', 10000)
        self.thread_count = 0
        self.lock = threading.RLock()
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # Bind the socket to the port
        print("Starting the connection at " + self.server_address[0])
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        self.sock.listen(5)
        while True:
            # Wait for a connection
            print('waiting for a connection')
            client, address = self.sock.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            threading.Thread(target=self.start_server, args=(client, address)).start()
            self.thread_count += 1
            print('Thread Number: ' + str(self.thread_count))
        self.sock.close()

    def start_server(self, client, client_address):
        client.sendall("connectionsuccess".encode())
        ext_status = False
        result = ""
        try:
            while not ext_status:
                # Receive the data in small chunks and retransmit it
                data = client.recv(1024)
                result = str(data).split("'")[1]
                
                result = result.split(";")
                if result[0] == "login":
                    message = self.get_login(result)
                    client.sendall(message.encode())
                elif result[0] == "apartment":
                    message = self.get_available_apartment(result)
                    client.sendall(message.encode())
                elif result[0] == "reservation":
                    message = self.set_reservation(result)
                    client.sendall(message.encode())
                elif result[0] == "report1":
                    message = self.get_report1()
                    client.sendall(message.encode())
                elif result[0] == "report2":
                    message = self.get_report2()
                    client.sendall(message.encode())
                elif result[0] == "report3":
                    message = self.get_report3()
                    client.sendall(message.encode())
                elif result[0] == "report4":
                    message = self.get_report4()
                    client.sendall(message.encode())
                else:
                    ext_status = True
                    break
        finally:
            # Clean up the connection
            client.close()
            self.thread_count -= 1

    def get_login(self,data):
        filename = "users.txt"
        with self.lock:
            try:
                with open(filename) as file:
                    for line in file:
                        line = line.strip("\n")
                        result = line.split(";")
                        if result[0] == data[1]:
                            if data[2] == result[1]:
                                return "loginsuccess;"+result[0]+";"+result[2]
                            else:
                                return "loginfailure"
                return "loginfailure"
            except:
                print("File could not opened!")


    def get_user(self, usarname):
        pass
    def set_reservation(self,data):
        filename = "reservations.txt"
        if self.get_apartment(data[1]) :
            if self.check_available(data[1], data[3], data[4]):
                new_data = "\n" + data[1] + ";" + data[2] +";"+ data[3] + ";" +data[4] + ";" +data[5]
                file = open(filename,"a")
                file.write(new_data)
                return "successfulreservation"
            else:
                return "notavailable"
        else:
             return "invalidapartmentcode"
        

    def get_available_apartment(self, data):
        apartment = self.get_apartment(data[1])
        if apartment:
            if self.check_available(data[1], data[2], data[3]):
                status = "Available"
            else:
                status = "Not Available"
            apartment += ";" + status
            return apartment
        else:
            return "invalidapartmentcode"

    def get_apartment(self, apart):
        filename = "apartments.txt"
        with self.lock:
            with open(filename) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    if result[0] == apart:
                        return line
        return None

    def check_available(self, apartment, start, end):
        filename = "reservations.txt"
        status = False
        with self.lock:
            with open(filename) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    if result[0] == apartment:
                        n_start = datetime.datetime.strptime(start, "%d/%m/%Y")
                        n_end = datetime.datetime.strptime(end, "%d/%m/%Y")
                        apt_start = datetime.datetime.strptime(result[2], "%d/%m/%Y")
                        apt_end = datetime.datetime.strptime(result[3], "%d/%m/%Y")
                        if (apt_start <= n_start <= apt_end) or (apt_start <= n_end <= apt_end):
                            status = False
                            return status
                        else:
                            status = True
                return status

    def get_report1(self):
        filename = "reservations.txt"
        count_list= list()
        with self.lock:
            with open(filename) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    count_list.append(result[4])
        return "report1;"+max(count_list,key=count_list.count)

    def get_report2(self):
        filename = "reservations.txt"
        count_list= list()
        with self.lock:
            with open(filename) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    count_list.append(result[0])
        return "report2;"+max(count_list,key=count_list.count)

    def get_report3(self):
        apart_list = list()
        today = datetime.date.today()
        today = today.strftime("%d/%m/%Y")
        count = 0
        filename = "apartments.txt"

        with self.lock:
            with open(filename) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    apart_list.append(result[0])
        for apart in apart_list:
            if self.check_available(apart, today, today):
                count += 1
        return "report3;"+str(count)
        
    def get_report4(self):
        apart_file_name = "apartments.txt"
        reserv_file_name = "reservations.txt"
        apart_list = list()
        count = 0
        with self.lock:
            with open(apart_file_name) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    apart_list.append(result[0])
        with self.lock:
            with open(reserv_file_name) as file:
                for line in file:
                    line = line.strip("\n")
                    result = line.split(";")
                    if result[0] in apart_list:
                        apart_list.remove(result[0])
        return "report4;"+str(len(apart_list))
        

def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
