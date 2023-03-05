#!/bin/bash

: '
    ---------------------------
    BEFORE RUNNING ON SERVER
    ---------------------------

    1. git clone to /tmp directory since permissions are good by default...
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

    7. if previous command did not run successfully, if statement is true
        if [[ $? != 0 ]]


    --------------------
    RESOURCES - main.sh
    --------------------

        1. exec > >(tee ${LOGGER}) 2>&1
            https://stackoverflow.com/questions/18460186/writing-outputs-to-log-file-and-console


    --------------------------
    RESOURCES - root_init.sh
    --------------------------
    
    1. grep -Fxq
        -F, --fixed-strings
            Interpret  PATTERN  as  a  list of fixed strings, separated by newlines, any of which is to be matched.
            (-F is specified by POSIX.)
        -x, --line-regexp
            Select only those matches that exactly match the whole line.  (-x is specified by POSIX.)
        -q, --quiet, --silent
            Quiet; do not write anything to standard output.  Exit immediately with zero status  if  any  match  is
                found,  even  if  an error was detected.  Also see the -s or --no-messages option.  (-q is specified by
                POSIX.)

    2. echo $SUDOERS_RULE | EDITOR='tee -a' visudo
        https://stackoverflow.com/questions/323957/how-do-i-edit-etc-sudoers-from-a-script


    3. why use visudo 
        https://unix.stackexchange.com/questions/27594/why-do-we-need-to-use-visudo-instead-of-directly-modifying-the-sudoers-file


    --------------------------
    RESOURCES - postgres.sh
    --------------------------

    1. $(cat ${1} | grep -iFn 'ipv4 local connections:' | cut -d ":" -f1)
        https://stackoverflow.com/questions/38990892/change-specific-line-and-row-in-text-file-in-bash

'

: '
    TODO:   
        1. postgres_init.sh 
            - add stuff to files saying lines were added by automation
'


LOG_DIR="logs"
LOG_FILE="main.log"
LOGGER="${PWD}/${LOG_DIR}/${LOG_FILE}"
exec > >(tee ${LOGGER}) 2>&1

# $1=permission integer
# $2=absolute path to file
function __chmod()
{
    sudo chmod $1 $2
}


# $1=user
# $2=group
# $3=absolute path to file
function __chown()
{
    sudo chown $1:$2 $3
}


# $1=postgres user
function check_if_postgres_user_exists()
{
    id -u $1
    if [[ $? != 0 ]]; then
        echo -e "\n'$1' user does not exist...exiting script'\n"
        exit 1
    fi
}


function now()
{
    TIMESTAMP=$(date +%s)
    HUMAN_READABLE_DATE=$(date -d @${TIMESTAMP})
    echo $HUMAN_READABLE_DATE
}


# $1=absolute path to root_init.sh
function run_root_init()
{
    echo -e "\nrunning '${1}' script\n"
    # sudo su -c "nohup ${SCRIPT_PATH}" # appends echo commands to file
    sudo "${1}"
}


# $1=absolute path to postgres_init.sh
function run_postgres_init()
{
    echo -e "\nrunning '${1}' script"
    sudo -u postgres $1
}




# INPUTS
SCRIPT_DIR="setup" # sudo chmod 745 ./setup
DEFAULT_CHMOD_INT=744
ROOT_SCRIPT="root_init.sh"
POSTGRES_SCRIPT="postgres_init.sh"


ROOT_USER="root"
ROOT_GROUP="root"
ROOT_SCRIPT_ABSPATH="${PWD}/${SCRIPT_DIR}/${ROOT_SCRIPT}"


POSTGRES_USER="postgres"
POSTGRES_GROUP="postgres"
POSTGRES_SCRIPT_ABSPATH="${PWD}/${SCRIPT_DIR}/${POSTGRES_SCRIPT}"


# METHOD CALLS 

# 1. start timestamp 
echo -e "SCRIPT START: $(now)\n\n"


# 2. run stuff root needs to do 
__chmod $DEFAULT_CHMOD_INT $ROOT_SCRIPT_ABSPATH
__chown $ROOT_USER $ROOT_GROUP $ROOT_SCRIPT_ABSPATH
run_root_init $ROOT_SCRIPT_ABSPATH


# 3. run stuff postgres needs to do
check_if_postgres_user_exists $POSTGRES_USER
__chmod $DEFAULT_CHMOD_INT $POSTGRES_SCRIPT_ABSPATH
__chown $POSTGRES_USER $POSTGRES_GROUP $POSTGRES_SCRIPT_ABSPATH
run_postgres_init $POSTGRES_SCRIPT_ABSPATH


# 4. start timestamp 
echo -e "SCRIPT END: $(now)\n\n"