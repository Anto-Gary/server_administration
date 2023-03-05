#!/bin/bash


# $1=absolute path to pg_hba.conf file 
# $2=IP address that postgres should accept connections from
function pg_set_allowed_ip()
{
    ALLOWED_HOSTS_LINENUM=$(cat ${1} | grep -iFn 'ipv4 local connections:' | cut -d ":" -f1)
    LINE_TO_REPLACE=$((ALLOWED_HOSTS_LINENUM + 1))

    # TODO: does not preserve spacing in row...
    awk -i inplace -v ipAddr="${2}" ' NR == "'"${LINE_TO_REPLACE}"'" {$4 = ipAddr} {print}' ${1}
}


# $1=absolute path to postgresql.conf file
# $2=interface PG should listen on (0.0.0.0/0 or localhost?)
function pg_set_listen_interface()
{
    PG_CONF_MATCH="# - Connection Settings -"

    LISTEN_INTERFACE_SECTION=$(cat ${1} | grep -Fn "${PG_CONF_MATCH}" | cut -d ":" -f1)
    LINE_TO_REPLACE=$((LISTEN_INTERFACE_SECTION + 2 ))

    sed -i "${LINE_TO_REPLACE}s/.*/${2}/" ${1}
}


# $1=new DB user
# $2=new DB user password
function pg_create_user()
{
    psql -c "CREATE USER ${1} WITH PASSWORD '${2}';"
}


# $1=new DB user
# $2=PG ROLE
function pg_add_role_to_user()
{
    psql -c "ALTER USER ${1} WITH ${2};"
}


# $1=name of new DB 
function pg_create_db()
{
    psql -c "CREATE DATABASE ${1};"
}


# maybe needed?
function pg_grant_user_db_privileges()
{
    psql -c "GRANT ALL PRIVILEGES ON DATABASE $2 TO $1;"
}


function pg_services()
{
    echo -e "\nstopping postgres service\n"
    sudo /bin/systemctl stop postgresql

    echo -e "\nstarting postgres service\n"
    sudo /bin/systemctl start postgresql

    echo -e "\ngetting postgres service status\n"
    sudo /bin/systemctl status postgresql
}


function pg_end()
{   
    echo -e "LIST ROLES\n"
    psql -c "\du+"

    echo -e "\n\n"

    echo -e "LIST DATABASES\n"
    psql -c "\l"
}



## INPUTS
POSTGRES_DIR="/etc/postgresql/14/main"

PG_HBA_CONF="pg_hba.conf"
PG_HBA_CONF_IP_ADDRESS="0.0.0.0/0" # TODO: should be IP of server, not everything...
PG_HBA_CONF_FULLPATH="${POSTGRES_DIR}/${PG_HBA_CONF}"


PG_CONF="postgresql.conf"
PG_CONF_LISTEN_ADDRESS="listen_addresses = '*'     # what IP address(es) to listen on;" # or localhost
PG_CONF_FULLPATH="${POSTGRES_DIR}/${PG_CONF}"

USER="wine_admin"
PASSWORD="super_strong_password"
DEFAULT_USER_ROLE="SUPERUSER"
DATABASE_NAME="wine_db"


# METHOD CALLS
pg_set_allowed_ip $PG_HBA_CONF_FULLPATH $PG_HBA_CONF_IP_ADDRESS
pg_set_listen_interface $PG_CONF_FULLPATH "$PG_CONF_LISTEN_ADDRESS" # needs quotes because there's spaces in variable...''

# # revert the command below using this: sudo -u postgres psql; DROP USER wine_admin; DROP DATABASE wine_db;
pg_create_user $USER $PASSWORD
pg_add_role_to_user $USER $DEFAULT_USER_ROLE
pg_create_db $DATABASE_NAME
pg_services
pg_end
# # pg_grant_user_db_privileges $USER $DATABASE_NAME
















# psql -h localhost -p 5432 -d db2 -U user2
# sudo passwd postgres SET PASSWORD FOR USER

# THIS IS SOME OF WHAT WOULD NEED TO BE DONE IF SCRIPT RUN AS UBUNTU, BUT DID STUFF ONLY POSTGRES USER CAN DO
# ALLOWED_HOSTS_LINENUM="$(sudo -i -u "postgres" bash -c 'echo ${POSTGRES_DIR} && ls -l && cat pg_hba.conf | grep -iFn "'"ipv4 local connections:"'" | cut -d ":" -f1 ')"
# TEST="$(sudo -i -u "postgres" bash -c 'cd "'"${POSTGRES_DIR}"'" && ls -l')" # -- DONT TOUCH
# ALLOWED_HOSTS_LINENUM="$(sudo -i -u "postgres" bash -c 'cd "'"${POSTGRES_DIR}"'" && cat "'"${PG_HBA_CONF}"'" | grep -iFn "'"ipv4 local connections:"'" | cut -d ":" -f1')"
# LINE_TO_REPLACE=$((ALLOWED_HOSTS_LINENUM + 1))
# sudo -u postgres psql --command '\password postgres'
# sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'newpassword';"
