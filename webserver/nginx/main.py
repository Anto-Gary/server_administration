from __future__ import annotations
import logging
import os

from conf.clsCfgs import get_nginx_class_config, get_reverse_proxy_config
from conf.logger import createLoggingConfig
from dotenv import load_dotenv
from logging.config import dictConfig
from run_code.NginxTemplater import NginxTemplater
from sys import exit

load_dotenv()

# GLOBAL VARIABLES 
LOGGER_NAME = os.getenv('LOGGER_NAME')
dictConfig(createLoggingConfig())
_LOGGER = logging.getLogger(LOGGER_NAME)


def create_reverse_proxy_template(nginx_cls_cfg, reverse_proxy_template_cfg):

    template_engine = NginxTemplater(nginx_cls_cfg)

    server_template = reverse_proxy_template_cfg['name']
    server_template_out = reverse_proxy_template_cfg['out_dir']
    server_template_ctx = reverse_proxy_template_cfg['context']
    template_engine.create_and_save_template(server_template, server_template_ctx, server_template_out)


if __name__ == "__main__":

    try: 
        _LOGGER.info("starting script")

        nginx_cls_cfg = get_nginx_class_config()
        reverse_proxy_template_cfg = get_reverse_proxy_config()

        create_reverse_proxy_template(nginx_cls_cfg, reverse_proxy_template_cfg)

        _LOGGER.info("ending script")

    except Exception as e:
        _LOGGER.exception("an unhandled exception occurred", exc_info=True)
        exit(1)