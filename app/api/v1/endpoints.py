from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile
from app.services.base_model_service import predict_label
from app.utils.file_checks import validate_txt_file, text_is_utf_8

router = APIRouter()

@router.post("/predict/base/")
async def predict(file: UploadFile = File(...), model_key: str = Form(...)):
    try:
        if not validate_txt_file(file):
            raise HTTPException(status_code=400, detail="Only plain text files (.txt) are supported")
        if not await text_is_utf_8(file):
            raise HTTPException(status_code=400, detail="Uploaded file must be UTF-8 encoded plain text")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = predict_label(tmp_path, model_type=model_key)

        return JSONResponse(content=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")