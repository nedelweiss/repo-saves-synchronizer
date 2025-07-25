import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def log_info(msg): logging.info(msg)
def log_warn(msg): logging.warning(msg)
def log_err(msg):  logging.error(msg)