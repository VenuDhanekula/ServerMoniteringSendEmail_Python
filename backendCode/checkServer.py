import socket
import ssl
from datetime import datetime
import pickle

import subprocess
import platform

from cfonts import render, say


class Server():
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()

        self.history = []
        self.alert = False

    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                #msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                msg = "{} is up. On port {} with {}".format(self.name,self.port,self.connection)
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                #msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                msg = "{} is up. On port {} with {}".format(self.name,self.port,self.connection)
                success = True
                self.alert = False
            else:
                if self.ping():
                    #msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                    msg = "{} is up. On port {} with {}".format(self.name,self.port,self.connection)
                    success = True
                    self.alert = False
        except socket.timeout:
            #msg = f"server: {self.name} timeout. On port {self.port}"
            msg = "server: {} timeout. On port {}".format(self.name,self.port)
        except (ConnectionRefusedError, ConnectionResetError) as e:
            #msg = f"server: {self.name} {e}"
            msg = "server: {} {}".format(self.name,e)
        except Exception as e:
            #msg = f"No Clue??: {e}"
            msg = "No Clue??: {}".format(e)

        
        if success == False and self.alert == False:
            # Send Alert
            self.alert = True

        self.create_history(msg,success,now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
                return False


def chechkServerFunction():
    try:
        while True:
            try:
                servers = pickle.load(open("/home/pi/backendCode/servers.pickle", "rb"))
            except:
                servers = [ 
                    Server("smtp.gmail.com", 465, "ssl", "high"),
                ]
                pickle.dump(servers, open("/home/pi/backendCode/servers.pickle", "wb"))
            servers = pickle.load(open("/home/pi/backendCode/servers.pickle", "rb"))
            for server in servers:
                server.check_connection()
                print(len(server.history))
                print(server.history[-1])

            pickle.dump(servers, open("/home/pi/backendCode/servers.pickle", "wb"))
                        
    except Exception as e:
        print(e)
