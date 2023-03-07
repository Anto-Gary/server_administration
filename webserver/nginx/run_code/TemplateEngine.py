from __future__ import annotations
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
import json
import logging
import os


class TemplateEngineException(Exception):
    """ default exception class for TemplateEngine """
    pass


class TemplateEngine:
    """
        - templates_dirname is configurable, template_context & template_out must already exist.
            1. templates_dirname - ./templates 
            2. template_context - ./templates/context
            3. template_out - ./templates/out
    """

    def __init__(self, config):
        self.TEMPLATE_DIR = config['template_dir']
        self.ENVIRONMENT = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR))
        self.LOGGER = logging.getLogger(config['logger_name'])

        # instance attributes
        self.TEMPLATE_OUT_DIR = os.path.join(self.TEMPLATE_DIR, "out")
        self.TEMPLATE_CONTEXT_DIR = os.path.join(self.TEMPLATE_DIR, "context")
        self.DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H-%M-%S'
        self.__check_dir_paths()


    def __check_dir_paths(self) -> None:
        """
            TEMPLATES_DIR/out & TEMPLATES_DIR/context must exist before this class can be used
        """

        self.__does_path_exist(self.TEMPLATE_OUT_DIR, "where templates are saved")
        self.__does_path_exist(self.TEMPLATE_CONTEXT_DIR, "where data to populate template is found")
        return


    def __does_path_exist(self, abspath: str, reason:str) -> None:
        """
            reason: why abspath needs to exist before using this class
        """

        if not os.path.exists(abspath):
            raise TemplateEngineException(f"'{abspath}' does not exist. directory is {reason}.")
        return


    def __create_template_out_subdir(self, directory: str, new_subdir: str) -> None:
        """
            directory: absolute path to .\\templates\\out
            new_subdir: template name without file extension

        returns C:\\.....\\templates\\out\\<new_subdir>
        """

        if not os.path.exists(directory):
            raise TemplateEngineException(f"'{directory}' must exist before creating subdirectory '{new_subdir}'")

        new_dir = os.path.join(directory, new_subdir)
        if not os.path.exists(new_dir): # new_dir isn't pushed to git
            os.makedirs(new_dir)

        return new_dir
    

    def __concat_rendered_template_out_abspath(self, out_dir: str, template_name: str) -> str:
        """
            out_dir: directory containing template results written by templater
            template_name: name of template being rendered, with extension

        returns: absolute path to template file guaranteed to be unique
        """

        now = datetime.now(timezone.utc)
        utc_now = now.strftime(self.DEFAULT_DATETIME_FORMAT)

        new_filename, extension = os.path.splitext(template_name)
        new_out_dir = self.__create_template_out_subdir(out_dir, new_filename)
        return os.path.join(new_out_dir, f"{new_filename}-{utc_now}{extension}")
    
    

    def __find_template_context(self, template_name: str):
        """
            template_name: expects there to be a file with the same name as template, minus extension, in ./templates/context
        """

        filename = os.path.splitext(template_name)[0]

        ctx_file_abspath = None
        for ctx_file in os.listdir(self.TEMPLATE_CONTEXT_DIR):
            ctx_name = os.path.splitext(ctx_file)[0]
            if ctx_name == filename:
                ctx_file_abspath = os.path.join(self.TEMPLATE_CONTEXT_DIR, ctx_file)
                break

        if not ctx_file_abspath:
            raise TemplateEngineException(f"'{template_name}' template must have a corresponding context file in '{self.TEMPLATE_CONTEXT_DIR}'")
        
        return self.__open_json(ctx_file_abspath)
    

    def __open_json(self, abs_path: str) -> str:
        """
            abs_path: absolute path to json file
        """
        with open(abs_path, "r") as j:
            data = json.load(j)
        return data


    def render_template(self, template_name) -> str:
        """
            template_name: name of template, no absolute path
        """

        curr_template = self.ENVIRONMENT.get_template(template_name)
        template_ctx = self.__find_template_context(template_name)
        return curr_template.render(template_ctx)
    

    def save_rendered_template(self, template_name: str, rendered_template: str) -> str:
        """
            template_name: absolute path where to save rendered template
            rendered_template: template that was rendered

        returns: saves a rendered template to ./templates/out/<template_name>/<template_name.extension>
        """

        template_out_dir = self.__concat_rendered_template_out_abspath(self.TEMPLATE_OUT_DIR, template_name)

        self.LOGGER.info(f"writing template to '{template_out_dir}'")
        with open(template_out_dir, mode="w", encoding="utf-8") as results:
            results.write(rendered_template)

        return template_out_dir