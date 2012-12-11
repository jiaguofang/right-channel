'''
Created on Dec 3, 2012

@author: Fang Jiaguo
'''
import logging.handlers
import os

project_root = os.path.dirname(os.path.dirname(__file__))

def get_logger(name, log_file):
    # Severity level: DEBUG/INFO/WARN/ERROR/CRITICAL
    logger = logging.getLogger(name)
    # Set to DEBUG when the application is under debugging, otherwise INFO.
    logger.setLevel(logging.DEBUG)
    # Create file handler with INFO log level accepting higher severity level than INFO.
    file_handler = logging.handlers.RotatingFileHandler(os.path.join(os.path.join(project_root, 'logs'), log_file), maxBytes=1024 * 1024 * 20)
    file_handler.setLevel(logging.INFO)
    # Create console handler with a higher DEBUG level accepting higher severity level than DEBUG.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # Add the handlers to logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger