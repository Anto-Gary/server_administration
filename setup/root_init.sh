#!/bin/bash


function __install_package()
{
    IS_PACKAGE_INSTALLED=$(dpkg -l | awk -v pkg="$1" ' $2 == pkg  ' | wc -l)
    if [[ IS_PACKAGE_INSTALLED -eq 0 ]]; then
        echo -e "installing package '${1}'\n"
        apt-get install $1 -y
    else
        echo -e "'${1}' package already installed on server\n"
    fi
}


function new_server_init()
{
    echo -e "getting updates..."
    apt-get update

    echo -e "doing upgrade..."
    apt-get upgrade -y    
}


function package_handler()
{
    PACKAGES=("$@")
    for PACKAGE in "${PACKAGES[@]}"; do
        __install_package $PACKAGE
    done
}


function set_sudoers()
{
    SUDOERS_RULES=("$@")
    for SUDOERS_RULE in "${SUDOERS_RULES[@]}"; do
        echo $SUDOERS_RULE | EDITOR='tee -a' visudo
    done
}


# INPUTS
SUDOERS_RULES=(
    "#### ADDED BY AUTOMATION SCRIPT #### "
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