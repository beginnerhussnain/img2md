from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from app.services.storage import save_upload, write_markdown
from app.services.ocr import run_ocr_hocr
from app.services.structure import parse_hocr, infer_markdown
from app.config import ALLOWED_MIME, MAX_FILE_SIZE, OUTPUT_DIR

router = APIRouter(prefix="/api", tags=["convert"])


@router.post("/image-to-markdown")
async def image_to_markdown(
    file: UploadFile = File(...),
    lang: str = Form("eng"),
):
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(400, f"Unsupported type: {file.content_type}")

    file_id, path = await save_upload(file)
    if path.stat().st_size > MAX_FILE_SIZE:
        path.unlink(missing_ok=True)
        raise HTTPException(413, "File too large")

    try:
        tree = run_ocr_hocr(path, lang=lang)
        lines = parse_hocr(tree)
        md = infer_markdown(lines)
    except Exception as e:
        raise HTTPException(500, f"OCR failed: {e}")

    write_markdown(file_id, md)
    return {"file_id": file_id, "markdown": md, "line_count": len(lines)}


@router.get("/download/{file_id}")
def download(file_id: str):
    p = OUTPUT_DIR / f"{file_id}.md"
    if not p.exists():
        raise HTTPException(404, "Not found")
    return FileResponse(p, media_type="text/markdown",
                        filename=f"{file_id}.md")