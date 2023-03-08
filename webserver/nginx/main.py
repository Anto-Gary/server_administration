from __future__ import annotations
import logging
import os

from conf.clsCfgs import get_nginx_class_config, get_reverse_proxy_config, get_systemd_service_config, get_http_load_balancing_config
from conf.logger import createLoggingConfig
from dotenv import load_dotenv
from logging.config import dictConfig
from run_code.NginxTemplater import NginxTemplater, NginxTemplaterException
from run_code.SystemdUnitFileTemplater import SystemdUnitFileTemplater, SystemdUnitFileTemplaterException
from run_code.TemplateEngine import TemplateEngineException

load_dotenv()

# GLOBAL VARIABLES 
LOGGER_NAME = os.getenv('LOGGER_NAME')
dictConfig(createLoggingConfig())
_LOGGER = logging.getLogger(LOGGER_NAME)


def create_reverse_proxy_template():

    nginx_cls_cfg = get_nginx_class_config()
    reverse_proxy_template_cfg = get_reverse_proxy_config()

    template_engine = NginxTemplater(nginx_cls_cfg)

    server_template = reverse_proxy_template_cfg['name']
    template_engine.create_reverse_proxy_template(server_template)


def create_http_load_balancing_template():

    
    nginx_cls_cfg = get_nginx_class_config()
    http_lb_cfg = get_http_load_balancing_config()

    template_engine = NginxTemplater(nginx_cls_cfg)

    template = http_lb_cfg['name']
    template_engine.create_http_load_balancing_template(template)


def create_systemd_service_unit_file_template():
    
    nginx_cls_cfg = get_nginx_class_config()
    systemd_unit_file_cfg = get_systemd_service_config()

    template_engine = SystemdUnitFileTemplater(nginx_cls_cfg)

    server_template = systemd_unit_file_cfg['name']
    template_engine.create_systemd_service_unit_file_template(server_template)


if __name__ == "__main__":

    try: 
        _LOGGER.info("starting script")

        create_reverse_proxy_template()
        # create_systemd_service_unit_file_template()
        create_http_load_balancing_template()
        

        _LOGGER.info("ending script")

    except TemplateEngineException as e:
        _LOGGER.exception("an exception was caught from template parent class", exc_info=True)
    except NginxTemplaterException as e: 
        _LOGGER.exception("an exception was caught from nginx template child class", exc_info=True)
    except SystemdUnitFileTemplaterException as e: 
        _LOGGER.exception("an exception was caught from systemd service unit file template child class", exc_info=True)
    except Exception as e:
        _LOGGER.exception("an unhandled exception occurred", exc_info=True)