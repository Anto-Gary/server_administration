from __future__ import annotations
from run_code.TemplateEngine import TemplateEngine
import logging


class SystemdUnitFileTemplaterException(Exception):
    """ default exception class for SystemdUnitFileTemplater """
    pass


class SystemdUnitFileTemplater(TemplateEngine):

    def __init__(self, config):
        super().__init__(config)
        self.LOGGER = logging.getLogger(config['logger_name'])


    def create_systemd_service_unit_file_template(self, template_name):
        """
            template_name: filename of template
        """

        # create template
        result = TemplateEngine.render_template(self, template_name)

        # save to ./templates/out/<template_name>
        return TemplateEngine.save_rendered_template(self, template_name, result)