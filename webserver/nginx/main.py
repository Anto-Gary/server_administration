from __future__ import annotations
import logging
import os

from conf.clsCfgs import get_nginx_class_config, get_reverse_proxy_config
from conf.logger import createLoggingConfig
from dotenv import load_dotenv
from logging.config import dictConfig
from run_code.NginxTemplater import NginxTemplater, NginxTemplaterException
from run_code.TemplateEngine import TemplateEngineException
from sys import exit

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


if __name__ == "__main__":

    try: 
        _LOGGER.info("starting script")

        create_reverse_proxy_template()

        _LOGGER.info("ending script")

    except TemplateEngineException as e:
        _LOGGER.exception("an exception was caught from template parent class", exc_info=True)
    except NginxTemplaterException as e:
        _LOGGER.exception("an exception was caught from template child class", exc_info=True)
    except Exception as e:
        _LOGGER.exception("an unhandled exception occurred", exc_info=True)
    finally:
        exit(1)