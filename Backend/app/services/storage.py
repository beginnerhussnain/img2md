import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from app.config import UPLOAD_DIR, OUTPUT_DIR


async def save_upload(file: UploadFile) -> tuple[str, Path]:
    file_id = uuid.uuid4().hex
    ext = Path(file.filename or "img.png").suffix or ".png"
    path = UPLOAD_DIR / f"{file_id}{ext}"
    async with aiofiles.open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)
    return file_id, path


def write_markdown(file_id: str, md: str) -> Path:
    out = OUTPUT_DIR / f"{file_id}.md"
    out.write_text(md, encoding="utf-8")
    return out