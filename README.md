# Getting Started
Following the below steps will set up a PostgreSQL docker container with the database and tables for the stock market predictor program scaffolded inside.  That said in order to complete the following steps locally, you will need to be on a machine with the following installed:

1. Liquibase
2. Docker
3. Git    

## Checkout the Repository Locally
Within a terminal, navigate to your workspace directory and run the following:
```git clone https://github.com/wynnblevins/predictor-db.git```

## PostgreSQL Docker Container
Next, once you have the predictor-db repository cloned locally, navigate inside the root of the project folder and run:
```docker run --rm --name pg-docker -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres``` 

Once the above command has completed, verify that you now have a PostgreSQL container called pq-docker running on your laptop.  You can view your local containers with the following command:
```docker container ls```

Next, run the following command to start a shell inside of your docker container:
```docker exec -it pg-docker bash```

Finally, log into the database by running the following command:
```psql -U postgres```

...and create the PostgreSQL database:
```CREATE DATABASE kafkatwitterstream```

Exit from the PostgreSQL terminal shell with:
```\q```

Then exit from the container and back to your "normal" shell by running:
```exit```

## Scaffold With Liquibase
In order to scaffold the database tables, run the following command:
```liquibase --driver=org.postgresql.Driver --classpath=postgresql-42.2.8.jar --changeLogFile="db/db.changelog-master.xml" --url=jdbc:postgresql://localhost:5432/kafkatwitterstream --username=postgres --password={PASSWORD} update```