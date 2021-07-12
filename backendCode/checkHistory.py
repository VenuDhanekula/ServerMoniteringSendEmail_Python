import pickle
from checkServer import Server

def checkHistoryData():
    servers = pickle.load(open( "/home/pi/backendCode/servers.pickle", "rb" ))

    for server in servers:
        server_up = 0
        for point in server.history:
            if point[1]:
                server_up += 1
        #print(f"----------\n{server.name} has been up {server_up / len(server.history) * 100}\nTotal History: {len(server.history)}\n----------\n")
        
        print("----------\n{} has been up {}\nTotal History: {}\n----------\n".format(server.name,server_up / len(server.history) * 100,len(server.history)))