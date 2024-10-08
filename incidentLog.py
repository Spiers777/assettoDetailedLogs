import json, sys, time

if __name__ == '__main__':
    from acplugins4python.ac_server_protocol import *
    from acplugins4python.ac_server_plugin import *

    global serverName, session

    def log(event, serverName, session):
        print("LOGGING")
        with open(f"./out/{serverName}_{session}.json", "r") as f:
            data = json.loads(f.read()) #Read existing Data
        incidentData = event.__dict__ #Get Incident Data in dict format
        incidentData["time"] = int(time.time() * 1000) # add epoch time data
        data["incidents"].append(incidentData) #Add incident to data
        with open(f"./out/{serverName}_{session}.json", "w") as f:
            f.write(json.dumps(data)) #Write data to file
        time.sleep(0.5)

    def callback(event):
        global serverName, session

        if type(event) in [NewSession, SessionInfo]:
            s.enableRealtimeReport(1000)
            serverName = event.serverName
            serverName = serverName.replace(" ", "_")
            session = event.name
            with open(f"./out/{serverName}_{session}.json", "w+") as f:
                f.write(json.dumps({"incidents": []}))
            print("Created Empty Log File")
        if "serverName" in globals():
            if type(event) == CollisionEnv:
                print("CollisionEnv")
                log(event, serverName, session)
            elif type(event) == CollisionCar:
                log(event, serverName, session)
            print(serverName)
    
    try:
        s = ACServerPlugin(int(sys.argv[1]), int(sys.argv[2]), callback) #standard = 12000, 8004
    except:
        s = ACServerPlugin(12000, 8004, callback) # Default to standard ports
        
    s.enableRealtimeReport(1000)

    while True:
        s.processServerPackets(3)