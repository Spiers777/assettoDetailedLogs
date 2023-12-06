import json, sys, time

if __name__ == '__main__':
    from acplugins4python.ac_server_protocol import *
    from acplugins4python.ac_server_plugin import *

    def processBuffer(buffer, serverName, session):
        with open (f"./out/{serverName}_{session}.json", "r") as f:
            data = json.loads(f.read())
        for event in buffer:
            data["incidents"].append(event)
        with open(f"./out/{serverName}_{session}.json", "w") as f:
            f.write(json.dumps(data))                     

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
                incidentData = event.__dict__
                incidentData["time"] = int(time.time() * 1000)
                buffer.append(incidentData)
            elif type(event) == CollisionCar:
                incidentData = event.__dict__
                incidentData["time"] = int(time.time() * 1000)
                buffer.append(incidentData)
    
    global serverName, session, buffer
    buffer = []

    try:
        s = ACServerPlugin(int(sys.argv[1]), int(sys.argv[2]), callback) #standard = 12000, 8004
    except:
        s = ACServerPlugin(12000, 8004, callback) # Default to standard ports
        
    s.enableRealtimeReport(1000)

    last_processed_time = time.time()
    while True:
        s.processServerPackets(3)
        if time.time() - last_processed_time >= 10: #Process and log buffer every 10 seconds
            if len(buffer) > 0:
                processBuffer(buffer, serverName, session)
                last_processed_time = time.time()
                buffer = []