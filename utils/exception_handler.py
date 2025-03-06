# utils/exception_handler.py
import logging

def handle_exception(exception):
    """
    Globally handles exceptions by logging them.
    """

    logging.exception(f"An unhandled exception occurred: {exception}")