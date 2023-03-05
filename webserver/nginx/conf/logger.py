import logging
import os
import time

from dotenv import load_dotenv
load_dotenv()

class UTCFormatter(logging.Formatter):
    converter = time.gmtime


class SecretsFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

 
    def filter(self, record):
      allow = True
      if self.param is not None and self.param in record.msg:
        allow = False

      return allow
    

def createLoggingConfig():
    # initEnv()
    loggerName = os.getenv("LOGGER_NAME")

    ENV = "production"
    isProd = ENV == "production"
    return {
        "version": 1,
            "formatters": {
                "default": {
                    '()': UTCFormatter,
                    "format": "%(asctime)s %(name)s[%(process)d] (%(module)s.%(funcName)s:%(lineno)s) - %(levelname)s: %(message)s",
                    "datefmt": "%m/%d/%Y %H:%M:%S"
                },
            },
        "filters": {
        "secretsFilter": {
            "()": SecretsFilter,
            "param": "password",
            }
        },
    "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["secretsFilter"]
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"logs/{loggerName}.log",
                "maxBytes": 50000000,
                "backupCount": 5,
                "formatter": "default",
                "filters": ["secretsFilter"]
            },
            # "smtp": {
            #     "class": "buffering_smtp_handler.BufferingSMTPHandler",
            #     "mailhost": "smtp_host.com",
            #     "fromaddr": "prod@donotreply.com" if isProd  else "nonprod@donotreply.com",
            #     "toaddrs":  [] if isProd else [],
            #     "subject": "TEST",
            #     "logging_format": "%(asctime)s %(name)s[%(process)d] (%(funcName)s:%(lineno)s) - %(levelname)s: %(message)s",
            #     "level": "ERROR",
            #     "capacity": 500,
            #     "filters": ["secretsFilter"]
            # }
        },
    "loggers": {
        loggerName: {
            "level": "INFO",
            # "handlers": ["console","file", "smtp"]
            "handlers": ["console","file"]
            }
        }
    }