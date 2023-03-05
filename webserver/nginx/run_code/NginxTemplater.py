from __future__ import annotations
import logging
import os

from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader


class NginxTemplaterException(Exception):
    """ default exception class for NginxTemplater """
    pass


class NginxTemplater:

    def __init__(self, config):
        self.LOGGER = logging.getLogger(config['logger_name'])

        # jinja stuff 
        self.ENVIRONMENT = Environment(loader=FileSystemLoader(config['templates_folder']))


    def create_template_result_save_path(self, out_dir: str, template_name: str) -> str:
        """
            out_dir: directory containing template results written by jinja2
            template_name: name of template being rendered, with extension

        returns: absolute path to template file guaranteed to be unique
        """

        default_save_extension = ".conf"
        now = datetime.now(timezone.utc)
        new_filename = os.path.splitext(template_name)[0]

        utc_now = now.strftime('%Y-%m-%dT%H-%M-%S')
        return os.path.join(out_dir, f"{new_filename}-{utc_now}{default_save_extension}")
    

    def save_template_result_to_fs(self, template_save_abspath: str, rendered_template: str) -> str:
        """
            template_save_abspath: absolute path where to save rendered jinja template
            rendered_template: template that was rendered

        returns: saves a rendered template to a specific directory
        """

        with open(template_save_abspath, mode="w", encoding="utf-8") as results:
            results.write(rendered_template)
            self.LOGGER.info(f"jinja template written to '{template_save_abspath}'")
        return template_save_abspath


    def create_reverse_proxy_template(self, reverse_proxy_template, reverse_proxy_template_ctx, reverse_proxy_template_out):
        """
            server_template: absolute path to template being used
            server_template_ctx: data being used in template
            server_template_out: absolute path to new template
        """

        # write template
        curr_template = self.ENVIRONMENT.get_template(reverse_proxy_template)
        jinja_result = curr_template.render(reverse_proxy_template_ctx)

        # save template to file
        reverse_proxy_template_out = self.create_template_result_save_path(reverse_proxy_template_out, reverse_proxy_template)
        return self.save_template_result_to_fs(reverse_proxy_template_out, jinja_result)