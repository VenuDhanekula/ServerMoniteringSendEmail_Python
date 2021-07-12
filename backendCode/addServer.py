import pickle
from checkServer import Server
from cfonts import render, say


def addServerData():
    try:
        servers = pickle.load(open("/home/pi/backendCode/servers.pickle", "rb"))
    except:
        servers = [ 
            Server("smtp.gmail.com", 465, "ssl", "high"),
        ]
        pickle.dump(servers, open("/home/pi/backendCode/servers.pickle", "wb"))


    ListOptions = ["1. Add a Server","2. Return"]

    for options in ListOptions:
        print(options)
        
    selection = (int(input("\n[INFO] ADD SERVER [1] / RETURN [2]:")))

    if (selection is 1):
        servername = raw_input("Enter The Server Name: ")
        port = int(raw_input("Enter a Port Number: "))
        connection = raw_input("Enter a Type ping/ plain/ ssl: ")
        priority = raw_input("Enter Priority high/low: ")

        new_server = Server(servername, port, connection, priority)
        servers.append(new_server)

        try:
            pickle.dump(servers, open("/home/pi/backendCode/servers.pickle", "wb" ))

        except:
            print("Error Occured While Saving The Server Details Please Restart")
            quit()
            
        else:
            output = render('Server Data Saved', font='console', colors=['red'], align='left')
            print(output)

    if (selection is 2):
        print("[INFO] Returning To Main Screen")
        pass
      
        
