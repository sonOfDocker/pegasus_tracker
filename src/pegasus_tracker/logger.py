import logging
import os

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler(os.path.join("logs", "pegasus.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
