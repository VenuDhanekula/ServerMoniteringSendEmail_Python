import socket
import ssl
from datetime import datetime
import pickle

import subprocess
import platform

import time

from cfonts import render, say

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


fromEmail = ""
fromEmailPassword = ""
toAddress = ""
sendMsg = ""
sendSubject = ""
sendAlert = False

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
            global sendAlert
            sendAlert = True

        self.create_history(msg,success,now)
        global sendMsg
        global sendSubject
        sendSubject = self.name + "Status"
        sendMsg = msg + "\n\n" + str(now)

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
            

    
def email_alert(subject, body):
    global fromEmail
    global fromEmailPassword
    global toAddress
    
    msg = MIMEMultipart('alternative')
    
    gmail_user = fromEmail
    gmail_password = fromEmailPassword
    msg['Subject'] = subject
    msg['From'] = fromEmail
    msg['To'] = toAddress

    # Create the body of the message (a plain-text and an HTML version).
    text = subject
    html = """
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           This is Venu Dhanekula<br>
           For any quaires you can contact me on below links<br>
           Here is the <a href="https://www.instagram.com">INSTAGRAM</a> you wanted.
           Here is the <a href="https://www.linkedin.com">LINKEDIN</a> you wanted.
           Here is the <a href="https://www.github.com">GITHUB</a> you wanted.
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    #For testing weather the data is reching or not
    #print(fromEmail+fromEmailPassword+subject+body+toAddress)
    # Send the message via SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.quit()

def chechkServerSendEmailFunction():
    fromEmail = raw_input("\nEnter Your Email Address: ")
    fromEmailPassword = raw_input("Enter Your Email Address Password: ")
    toAddress = raw_input("Enter To Email Address: ")
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
                print("")
                print(len(server.history))
                print(server.history[-1])
                
                global sendAlert
                global sendMsg
                global sendSubject
                if(sendAlert == True):
                    email_alert(sendSubject, sendMsg)

            pickle.dump(servers, open("/home/pi/backendCode/servers.pickle", "wb"))
            time.sleep(2)
                        
    except Exception as e:
        print(e)
