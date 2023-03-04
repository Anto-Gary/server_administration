#!/bin/bash

: '
    ---------------------------
    BEFORE RUNNING ON SERVER
    ---------------------------

    1. install git 
'

: '
    -----------------
    RANDOM COMMANDS 
    -----------------
    
    1. change default editor from nano to vim

        a) sudo update-alternatives --config editor
            choose vim.basic

        b) use EDITOR environment variable to choose
            sudo EDITOR=nano visudo /etc/sudoers

    2. check if visudo has proper syntax to be used 
        visudo -c -f /etc/sudoers

    3. list packages 
         sudo dpkg-query -l | grep postgres
         sudo apt list --installed | grep postgres

    4. switch user command
        sudo -i -u postgres
        sudo -su postgres

    5. delete line in vim 
        vdd + d

    6. make sure postgres running on correct interface 
        ss -nlt | grep 5432

    ------------
    RESOURCES 
    ------------
        1. why use visudo 
            https://unix.stackexchange.com/questions/27594/why-do-we-need-to-use-visudo-instead-of-directly-modifying-the-sudoers-file
'

: '
    TODO:   
        1.
'


# $1 = permission integer
# $2 = absolute path to file
function __chmod()
{
    sudo chmod $1 $2    
}


# $1 = user
# $2 = group
# $3 = absolute path to file
function __chown()
{
    sudo chown $1:$2 $3
}


# $1 = user
# $2 = group
# $3 = chmod integer
# $4 = absolute path to file
function set_permission_and_ownership()
{
    __chmod $3 $4
    __chown $1 $2 $4
}


function run_root_init()
{
    echo -e "running '${1}' script"
    # sudo su -c "nohup ${SCRIPT_PATH}" # appends echo commands to file
    sudo "${1}"
}

function run_postgres_init()
{
    echo -e "running '${1}' script"
    sudo -u postgres $1
}


# INPUTS
SCRIPT_DIR="setup" # sudo chmod 745 ./setup
DEFAULT_CHMOD=744
ROOT_SCRIPT="root_init.sh"
POSTGRES_SCRIPT="postgres_init.sh"


ROOT_USER="root"
ROOT_GROUP="root"
ROOT_SCRIPT_ABSPATH="${PWD}/${SCRIPT_DIR}/${ROOT_SCRIPT}"


POSTGRES_USER="postgres"
POSTGRES_GROUP="postgres"
POSTGRES_SCRIPT_ABSPATH="${PWD}/${SCRIPT_DIR}/${POSTGRES_SCRIPT}"


# METHOD CALLS 
set_permission_and_ownership $ROOT_USER $ROOT_GROUP $DEFAULT_CHMOD $ROOT_SCRIPT_ABSPATH
run_root_init $ROOT_SCRIPT_ABSPATH

set_permission_and_ownership $POSTGRES_USER $POSTGRES_GROUP $DEFAULT_CHMOD $POSTGRES_SCRIPT_ABSPATH # MUST BE RUN AFTER POSTGRES INSTALLED 
run_postgres_init $POSTGRES_SCRIPT_ABSPATH