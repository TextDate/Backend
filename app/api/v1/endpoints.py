from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.base_model_service import predict_base_label
from app.services.binary_model_service import predict_binary_label
from app.utils.file_checks import validate_file

router = APIRouter()

@router.post("/predict/base/")
async def predict(file: UploadFile = File(...), model_key: str = Form(...)):
    try:
        tmp_path = await validate_file(file)
        result = predict_base_label(tmp_path, model_type=model_key)

        return JSONResponse(content=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/predict/binary/")
async def predict(file: UploadFile = File(...), model_key: str = Form(...), threshold: int = Form(...)):
    try:
        tmp_path = await validate_file(file)
        result = predict_binary_label(tmp_path, model_type=model_key, threshold=threshold)

        return JSONResponse(content=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")