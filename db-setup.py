import os
import time 
import sys 
import ConfigParser

def startDockerContainer(): 
    # create a docker container
    os.system('docker run -p 5432:5432 --name personalpostgres -e POSTGRES_PASSWORD=postgres -d postgres:9.6')
    time.sleep(10)

def createDatabase():
    config = ConfigParser.RawConfigParser()
    config.read('db.properties')

    os.system("docker exec -it personalpostgres createdb -U postgres -h localhost -w predictor_db")
    os.system('liquibase --classpath=' + config.get("database", "CLASSPATH") + ' --changeLogFile="./db/db.changelog-master.xml" --driver="org.postgresql.Driver" --url="jdbc:postgresql://10.0.0.228:5432/predictor_db" --username=postgres --password=postgres update')

def pgup():
    print("Starting...")
    startDockerContainer()
    createDatabase()

def pgdown(): 
    print("Stopping...")
    os.system('docker stop personalpostgres')

def pgnuke(): 
    print("Removing...")
    os.system('docker rm personalpostgres -f')

def pgrestart(): 
    print("Restarting...")
    os.system('docker restart personalpostgres')
    
def pgupdate():
    scaffoldDatabases()

def delegateCommand():
    print('inside delegate command')
    
    switcher = {
        "stop": pgdown,
        "remove": pgnuke,
        "start": pgup,
        "restart": pgrestart,
        "update": pgupdate
    }
    if (len(sys.argv) == 2):
        command = sys.argv[1]

        # Get the function from switcher dictionary
        func = switcher.get(command, lambda: "Invalid command! \nUsage: " + 
            sys.argv[0] + " {start|stop|restart|remove|update}")
        # Execute the function
        print(func())

delegateCommand()

