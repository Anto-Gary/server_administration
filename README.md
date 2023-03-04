# POSTGRES INSTALL SCRIPT 

- this is a script to setup postgres server on EC2 ubuntu instance


### WHAT
---

1. ./main.sh

    - sets permissions on 2 shell scripts in ./setup dirctory & runs them

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


### HOW 
---

1. ./main.sh