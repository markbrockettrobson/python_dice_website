import logging


def _set_up_root_logger():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] %(name)30s | %(levelname)10s | %(message)s"
    )
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger("PDWA")
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    return root_logger


ROOT_LOGGER = _set_up_root_logger()
