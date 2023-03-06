from __future__ import annotations
import json
import os
from dotenv import load_dotenv

abspath_env = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.env'))
load_dotenv(abspath_env)

# START ENVIRONMENT VARIABLES 
LOGGER_NAME = os.getenv('LOGGER_NAME')

TEMPLATES_MAIN_DIR = os.getenv('TEMPLATES_MAIN_DIR')
TEMPLATES_OUT_DIR = os.getenv('TEMPLATES_OUT_DIR')
TEMPLATES_CONFIG_DIR = os.getenv('TEMPLATES_CONFIG_DIR')

NGINX_REVERSE_PROXY_TEMPLATE = os.getenv('NGINX_REVERSE_PROXY_TEMPLATE')
NGINX_REVERSE_PROXY_CONFIG = os.getenv('NGINX_REVERSE_PROXY_CONFIG')
# END ENVIRONMENT VARIABLES 


# START GLOBAL VARIABLES 
TEMPLATES_MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, TEMPLATES_MAIN_DIR))
TEMPLATES_OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, TEMPLATES_MAIN_DIR, TEMPLATES_OUT_DIR))
TEMPLATES_CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, TEMPLATES_MAIN_DIR, TEMPLATES_CONFIG_DIR))
# END GLOBAL VARIABLES 


# __init__ config for NginxTemplater class 
def get_nginx_class_config():
    return {
        "templates_folder": TEMPLATES_MAIN_DIR,
        "logger_name": LOGGER_NAME
    }


# all data needed for NginxTemplater.create_reverse_proxy_template method
def get_reverse_proxy_config():
    reverse_proxy_template_config_abspath = os.path.join(TEMPLATES_CONFIG_DIR, NGINX_REVERSE_PROXY_CONFIG)
    reverse_proxy_template_ctx = __open_json(reverse_proxy_template_config_abspath)
    return {
        "name": NGINX_REVERSE_PROXY_TEMPLATE,
        "out_dir": TEMPLATES_OUT_DIR,
        "context": reverse_proxy_template_ctx
    }


# helper method
def __open_json(abs_path):
    """
        abs_path: absolute path to json file
    """
    with open(abs_path, "r") as j:
        data = json.load(j)
    return data