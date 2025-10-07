import os
from logging import Logger
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT").strip()
    LOGGING_DIR = Path(os.path.abspath("logs"))
    LOGGER: Optional[Logger] = None
