import mimetypes
import tempfile

from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)


async def text_is_utf_8(file: UploadFile) -> bool:
    """Check if an uploaded file is UTF-8 encoded."""
    sample = await file.read()
    await file.seek(0)
    try:
        sample.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def validate_txt_file(file: UploadFile) -> bool:
    """Check if file has a MIME type of plain text."""
    mime_type, _ = mimetypes.guess_type(file.filename)
    return mime_type == "text/plain"


async def validate_file(file: UploadFile) -> str:
    if not validate_txt_file(file):
        raise HTTPException(status_code=400, detail="Only plain text files (.txt) are supported.")

    if not await text_is_utf_8(file):
        raise HTTPException(status_code=400, detail="Uploaded file must be UTF-8 encoded.")

    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as tmp:
            tmp.write(contents)
            return tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process uploaded file: {str(e)}")

def text_trimmer(text_path: str) -> str:
    """
    Open and sanitize text file content.
    Removes unwanted whitespace and filters out non-allowed characters.
    Returns cleaned string, or empty string on failure.
    """
    if not text_path:
        return ""

    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()

        substitutions = {
            '\n': ' ',
            '\r': ' ',
            '\t': ' ',
        }
        for old, new in substitutions.items():
            text = text.replace(old, new)

        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            " .,!?;:'\"()[]{}<>@#$%^&*-+=_/\\|~`"
        )

        return ''.join(c for c in text if c in allowed_chars)

    except Exception as e:
        logger.error(f"[text_trimmer] Failed to process {text_path}: {e}")
        return ""