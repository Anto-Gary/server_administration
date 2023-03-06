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


    def __create_new_out_subdir(self, directory: str, new_subdir: str) -> None:
        """
            directory: absolute path to .\\templates\\out
            new_subdir: template name without file extension

        returns C:\\.....\\templates\\out\\<template_name>
        """

        if not os.path.exists(directory):
            raise NginxTemplaterException(f"'{directory}' must exist before creating subdirectory'{new_subdir}'")

        new_dir = os.path.join(directory, new_subdir)
        if not os.path.exists(new_dir):
            # only executed when script first runs, folder isn't pushed to git
            os.makedirs(new_dir)

        return new_dir


    def create_template_result_save_path(self, out_dir: str, template_name: str) -> str:
        """
            out_dir: directory containing template results written by jinja2
            template_name: name of template being rendered, with extension

        returns: absolute path to template file guaranteed to be unique
        """

        default_save_extension = ".conf"
        now = datetime.now(timezone.utc)
        utc_now = now.strftime('%Y-%m-%dT%H-%M-%S')

        new_filename = os.path.splitext(template_name)[0]
        new_out_dir = self.__create_new_out_subdir(out_dir, new_filename)

        return os.path.join(new_out_dir, f"{new_filename}-{utc_now}{default_save_extension}")
    

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


    def write_template(self, template_name: str, template_ctx) -> str:
        """
            template_name: name of template, no absolute path
            template_ctx: data that corresponds to template_name
        """

        curr_template = self.ENVIRONMENT.get_template(template_name)
        return curr_template.render(template_ctx)


    def create_and_save_template(self, template_name, template_ctx, template_out):
        """
            template_name: filename of template
            template_ctx: data being used in template_name
            template_out: absolute path to 'template out' directory
        """

        # write template
        result = self.write_template(template_name, template_ctx)

        # create save path & save template to file
        new_out_dir = self.create_template_result_save_path(template_out, template_name)
        return self.save_template_result_to_fs(new_out_dir, result)