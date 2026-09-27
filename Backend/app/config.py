from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp", "image/tiff"}

# Auto-delete files older than this many minutes
FILE_RETENTION_MINUTES = 30
# How often the background sweeper runs (seconds)
CLEANUP_INTERVAL_SECONDS = 60

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_MIME = {"image/png", "image/jpeg", "image/webp", "image/tiff"}