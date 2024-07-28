from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

DATE_FORMAT: str = "%Y-%m-%d"

LOG_DIR: Path = BASE_DIR / "logs"
LOG_FORMAT: str = '"%(asctime)s - [%(levelname)s] - %(message)s"'
