from cfonts import render, say
import sys

output = render('Server Testing|Service',font='chrome', gradient=['red', 'yellow'], align='center')
print(output)


ListOptions = ["1. Add a Server","2. Check Server Status","3. Check Server Status And Send Email","4. Check History","5. Quit"]

print("\n[INFO] Pre Defined Server = Server Name: smtp.gmail.com, Port: 465 , Type: ssl , Priority: high")

while True:
    output = render('[INFO] SELECT AN OPTION:', font='console', colors=['red'], align='left')
    print(output)
    for options in ListOptions:
        print(options)
    selection = (int(input("\n[INFO] SELECT A OPTION [1 - 5]:")))

    if (selection is 1):
        sys.path.append('/home/pi/backendCode')
        import addServer
        addServer.addServerData()
        
    if (selection is 2):
        try:
            sys.path.append('/home/pi/backendCode')
            import checkServer
            checkServer.chechkServerFunction()
        except Exception as e:
            print(e)
            
    if (selection is 3):
        try:
            sys.path.append('/home/pi/backendCode')
            import checkServerSendEmail
            checkServerSendEmail.chechkServerSendEmailFunction()
        except Exception as e:
            print(e)
        
    if (selection is 4):
        try:
            sys.path.append('/home/pi/backendCode')
            import checkHistory
            checkHistory.checkHistoryData()
        except Exception as e:
            print(e)
            quit()
        
    if (selection is 5):
        output = render('\nTHANKS FOR USING|[LINK] https://github.com/VenuDhanekula', font='console', colors=['red'], align='left')
        print(output)
        quit()
