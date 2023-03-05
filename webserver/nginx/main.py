from __future__ import annotations
import logging
import os

from conf.logger import createLoggingConfig
from dotenv import load_dotenv
from logging.config import dictConfig
from run_code.NginxTemplater import NginxTemplater
from sys import exit

load_dotenv()

# GLOBAL VARIABLES 
LOGGER_NAME = os.getenv('LOGGER_NAME')
JINJA_TEMPLATES_FOLDER = os.getenv('JINJA_TEMPLATES_FOLDER')
NGINX_REVERSE_PROXY_TEMPLATE = os.getenv('NGINX_REVERSE_PROXY_TEMPLATE')

dictConfig(createLoggingConfig())
_LOGGER = logging.getLogger(LOGGER_NAME)


# METHODS
def create_reverse_proxy_template(logger_name, jinja_templates_folder, reverse_proxy_template):

    # directory that contains jinja templates
    abs_path_templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), jinja_templates_folder))

    # jinja templates save path
    reverse_proxy_template_out = os.path.abspath(os.path.join(os.path.dirname(__file__), jinja_templates_folder, "out"))

    # template class config 
    nginx_cls_cfg = {
        "templates_folder": abs_path_templates_dir,
        "logger_name": logger_name
    }

    # ONLY THING THAT CHANGES
    reverse_proxy_template_ctx = {
        "server": {
            "listen": 80,
            "server_name": "www.summry.me",
            "root": "/home/ubuntu/net_core/net_core_boilerplate",
            "location": {
                "proxy_pass": "http://localhost:5000",
            }
        }
    }
    
    reverse_proxy_template_cfg = {
        "name": reverse_proxy_template,
        "out_dir": reverse_proxy_template_out,
        "context": reverse_proxy_template_ctx
    }

    # START CODE 
    template_engine = NginxTemplater(nginx_cls_cfg)

    server_template = reverse_proxy_template_cfg['name']
    server_template_out = reverse_proxy_template_cfg['out_dir']
    server_template_ctx = reverse_proxy_template_cfg['context']
    template_engine.create_reverse_proxy_template(server_template, server_template_ctx, server_template_out)



# INIT
if __name__ == "__main__":

    try: 
        _LOGGER.info("starting script")

        create_reverse_proxy_template(LOGGER_NAME, JINJA_TEMPLATES_FOLDER, NGINX_REVERSE_PROXY_TEMPLATE )

        _LOGGER.info("ending script")

    except Exception as e:
        _LOGGER.exception("an unhandled exception occurred", exc_info=True)
        exit(1)