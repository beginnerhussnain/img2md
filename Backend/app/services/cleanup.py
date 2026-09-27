import asyncio
import time
from app.config import (
    UPLOAD_DIR, OUTPUT_DIR,
    FILE_RETENTION_MINUTES, CLEANUP_INTERVAL_SECONDS,
)


def _sweep_once() -> int:
    """Delete files older than retention. Returns count deleted."""
    cutoff = time.time() - FILE_RETENTION_MINUTES * 60
    deleted = 0
    for folder in (UPLOAD_DIR, OUTPUT_DIR):
        for f in folder.iterdir():
            if not f.is_file():
                continue
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
                    deleted += 1
            except OSError:
                pass
    return deleted


async def cleanup_loop():
    """Run forever in the background. Started on app startup."""
    while True:
        try:
            n = _sweep_once()
            if n:
                print(f"[cleanup] deleted {n} expired file(s)")
        except Exception as e:
            print(f"[cleanup] error: {e}")
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)