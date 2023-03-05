#!/bin/bash

# $1=name of package to be installed
function __install_package()
{
    IS_PACKAGE_INSTALLED=$(dpkg -l | awk -v pkg="$1" ' $2 == pkg  ' | wc -l)
    if [[ IS_PACKAGE_INSTALLED -eq 0 ]]; then
        echo -e "\ninstalling package '${1}'\n"
        apt-get install $1 -y
    else
        echo -e "\n'${1}' package already installed on server\n"
    fi
}


function new_server_init()
{
    echo -e "\ngetting system updates...\n"
    apt-get update

    echo -e "\ndoing system upgrade...\n"
    apt-get upgrade -y    
}


# $@=list of packages to be installed on server
function package_handler()
{
    PACKAGES=("$@")
    for PACKAGE in "${PACKAGES[@]}"; do
        __install_package $PACKAGE
    done
}


# $@=list of sudoers rules to be added to sudoers file
function set_sudoers()
{
    SUDOERS_FILE="/etc/sudoers"

    SUDOERS_RULES=("$@")
    for SUDOERS_RULE in "${SUDOERS_RULES[@]}"; do
        grep -Fxq "$SUDOERS_RULE" $SUDOERS_FILE
        if [[ $? != 0 ]]; then
            echo -e "\nadding sudoers rule '${SUDOERS_RULE}' to '${SUDOERS_FILE}'\n"
            echo $SUDOERS_RULE | EDITOR='tee -a' visudo
        fi
    done
}



# INPUTS 
SUDOERS_RULES=(
    "#### ADDED BY AUTOMATION SCRIPT ####"
    "postgres  ALL=(ALL:ALL) NOPASSWD: /bin/systemctl start postgresql"
    "postgres  ALL=(ALL:ALL) NOPASSWD: /bin/systemctl stop postgresql"
    "postgres  ALL=(ALL:ALL) NOPASSWD: /bin/systemctl status postgresql"
    "postgres  ALL=(ALL:ALL) NOPASSWD: /bin/journalctl -xe"
)


PACKAGES=(
    "postgresql" 
    "postgresql-contrib"
    )


# METHOD CALLS 
new_server_init
package_handler "${PACKAGES[@]}"
set_sudoers "${SUDOERS_RULES[@]}"