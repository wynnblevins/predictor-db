import os
import time 
import sys 
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('db.properties')

def startDockerContainer(): 
    # create a docker container
    os.system('docker run -p 5432:5432 --name ' + config.get("database", "CONTAINER_NAME") + ' -e POSTGRES_PASSWORD=postgres -d postgres:9.6')
    time.sleep(10)

def createDatabase():
    command = 'liquibase --classpath=' + config.get("database", "CLASSPATH") + ' --changeLogFile="./db/db.changelog-master.xml" --driver="org.postgresql.Driver" --url="jdbc:postgresql://' + config.get("database", "IP") + ':5432/' + config.get("database", "DATABASE") + '" --username=' + config.get("database", "USERNAME") + ' --password=' + config.get("database", "PASSWORD") + ' update'
    print(command)
    
    os.system("docker exec -it " + config.get("database", "CONTAINER_NAME") + " createdb -U postgres -h localhost -w " + config.get("database", "DATABASE"))
    os.system('liquibase --classpath=' + config.get("database", "CLASSPATH") + ' --changeLogFile="./db/db.changelog-master.xml" --driver="org.postgresql.Driver" --url="jdbc:postgresql://' + config.get("database", "IP") + ':5432/' + config.get("database", "DATABASE") + '" --username=' + config.get("database", "USERNAME") + ' --password=' + config.get("database", "PASSWORD") + ' update')

def pgup():
    print("Starting...")
    startDockerContainer()
    createDatabase()

def pgdown(): 
    print("Stopping...")
    os.system('docker stop ' + config.get("database", "CONTAINER_NAME"))

def pgnuke(): 
    print("Removing...")
    os.system('docker rm ' + config.get("database", "CONTAINER_NAME") + ' -f')

def pgrestart(): 
    print("Restarting...")
    os.system('docker restart ' + config.get("database", "CONTAINER_NAME"))
    
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

