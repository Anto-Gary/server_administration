# POSTGRES INSTALL SCRIPT 

- this is a script to setup postgres server on EC2 ubuntu instance


### WHAT
---

1. ./main.sh

    - sets permissions on 2 shell scripts in ./setup dirctory & runs them

    - logs written to ./logs/main.log

    - after running script, you should set password for postgres user 

        a. ./setup/root_init.sh

            - can only be run as root user

            - update server 

            - install postgres packages

            - alllow postgres user to run certain systemctl commands for DB 


        b. ./setup/postgres_init.sh

            - can only be run as postgres user
  
            - set allowed IPs for postgres to talk to

            - set interface postgres is listening on 

            - create new postgres user with password

            - assign new postgres user a role

            - create database 
    

2. result of script is: 
   
   - a new postgres superuser user w/ password

   - a new DB 

     - thats listening on 0.0.0.0:5432 

       - which accepts ipv4 connections from anywhere 

       - API can read/write to it but should limit to API server IP

### PREREQUISITES 
---

1. git 

   - sudo apt-get install git


2. ssh-keygen 
   
    - cat ~/.ssh/id_rsa.pub
    
      - copy output to github profile 


3. git clone to /tmp directory 

   - because postgres user doesn't have permissions to /home/ubuntu by default


4. postgres DB schema should be 'public' unless there's a good reason not to 


### BEFORE RUNNING SCRIPT - VARIABLES TO CONSIDER
---

1. ./main.sh

   - LOG_DIR = log file directory 


   - LOG_FILE = log file name

2. ./setup/postgres_init.sh 


   - PG_HBA_CONF_IP_ADDRESS = IP postgres accepts connections from 


   - PG_CONF_LISTEN_ADDRESS = interface on which postgres listens 


   - USER = new postgres user


   - PASSWORD = password for new postgres user


   - DEFAULT_USER_ROLE = defaults to SUPERUSER, must be an existing postgres role 


   - DATABASE_NAME = name of new DB


3. ./setup/root_init.sh

   - SUDOERS_RULES = additional sudoers rules postgres user should have 