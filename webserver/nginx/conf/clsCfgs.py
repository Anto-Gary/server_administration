from __future__ import annotations
from dotenv import load_dotenv
import os

abspath_env = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.env'))
load_dotenv(abspath_env)


# START ENVIRONMENT VARIABLES 
ENV_LOGGER_NAME = os.getenv('LOGGER_NAME')
ENV_TEMPLATES_MAIN_DIR = os.getenv('TEMPLATES_MAIN_DIR')
ENV_NGINX_REVERSE_PROXY_TEMPLATE = os.getenv('NGINX_REVERSE_PROXY_TEMPLATE')
ENV_NGINX_HTTP_LOAD_BALANCING_TEMPLATE = os.getenv('NGINX_HTTP_LOAD_BALANCING_TEMPLATE')
ENV_SYSTEMD_UNIT_FILE_TEMPLATE = os.getenv('SYSTEMD_UNIT_FILE_TEMPLATE')
# END ENVIRONMENT VARIABLES 


# START GLOBAL VARIABLES
TEMPLATES_MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, ENV_TEMPLATES_MAIN_DIR))
# END GLOBAL VARIABLES 


# __init__ config for NginxTemplater class 
def get_nginx_class_config():
    return {
        "template_dir": TEMPLATES_MAIN_DIR,
        "logger_name": ENV_LOGGER_NAME
    }


def get_reverse_proxy_config():
    return {
        "name": ENV_NGINX_REVERSE_PROXY_TEMPLATE
    }


def get_systemd_service_config():
    return {
        "name": ENV_SYSTEMD_UNIT_FILE_TEMPLATE
    }


def get_http_load_balancing_config():
    return {
        "name": ENV_NGINX_HTTP_LOAD_BALANCING_TEMPLATE
    }