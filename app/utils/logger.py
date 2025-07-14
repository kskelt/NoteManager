import logging
from app.core.settings import get_settings

settings = get_settings()
logger = logging.getLogger("notes_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(settings.log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def log_action(username: str, role: str, action: str, target_id: str | None = None):
    message = f"{username} with role {role} performed {action}"
    if target_id:
        message += f" on {target_id}"
    logger.info(message)
