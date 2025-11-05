# mobile-network-analytics

Application for calculating mobile subscriber and network statistics from raw data

# How to use

### Requirements

a. Docker

### Steps

1. Create a .env file like below

   ```
   DB_USERNAME=mariadb
   DB_PASSWORD=mariadb
   DB_NAME=mariadb
   DB_HOST=localhost
   # DB_HOST=mariadb
   DB_PORT=3306

   DIRECTORY_PATH=./data
   END_TIME='2017-03-01 08:05:00'
   ```

   For this step you need to set host to "localhost"

2. Run `docker compose up -d mariadb` to start the database container

3. Export the .env variables on a terminal window and run the script in the scripts folder to create the db tables.
   `python scripts/init_db.py`

4. Update the .env and comment the `DB_HOST=localhost` and uncomment the `DB_HOST=mariadb` line. This is because, unlike the terminal, Docker cannot access localhost and needs the container name.

5. Run `docker build -t mobile_network_analytics:latest .` and then `docker compose up -d` to start all the containers.

After the above steps the celery job will start to run. You will need to place the sample files in the directory spcecified in the .env file in order to be found. If a directory outside the project's directory is specified, it will probably need to be mounted to Docker (let's leave that for now).

The job will look for files according to `END_TIME='2017-03-01 08:05:00'`. This sample time corresponds to the sample files' time. Docker runs on ETC time.

If the above .env variable is not set, the job will run looking for files based on the current time of the system.

The job is scheduled to run every five minutes and every hour (1 minute after the file generation is completed)

6. After a single run of the job, you can use the API and `localhost:5000` to get the KPI results from the two endpoints.
