from fastapi import HTTPException
from pydantic import BaseModel, validator
from uuid import UUID
from typing import Optional

class HeartDiseaseResponse(BaseModel):
    uuid: UUID
    proba: float


class HeartDiseaseRequest(BaseModel):
    uuid: Optional[UUID]      
    sex: int
    cp: int
    fbs: int
    restecg: int
    exang: int
    slope: int
    ca: int
    thal: int
    age: int
    trestbps: int
    chol: int
    thalach: int
    oldpeak: float


    @validator("sex", "fbs", "exang")
    def validadte_binary_features(cls, value, field):
        if value not in (0, 1):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Value should be binary: 1 or 0"
            )
        return value


    @validator("age")
    def validadte_age(cls, value, field):
        if not (0 < value <= 150):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Bad value: {value}"
            )
        return value


    @validator("trestbps", "thalach")
    def validadte_trestbps_thalach(cls, value, field):
        if not (40 <= value <= 230):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Value should be in [40 : 230]"
            )
        return value


    @validator("restecg", "slope")
    def validadte_restecg_slope(cls, value, field):
        if value not in (0, 1, 2):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Value should be one of [0, 1, 2]"
            )
        return value


    @validator("cp", "thal")
    def validadte_cp_thal(cls, value, field):
        if value not in (0, 1, 2, 3):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Value should be one of [0, 1, 2, 3]"
            )
        return value


    @validator("ca")
    def validadte_ca(cls, value, field):
        if value not in (0, 1, 2, 3, 4):
            raise HTTPException(
                status_code=400,
                detail=f"{field.name}: Value should be one of [0, 1, 2, 3, 4]"
            )
        return value

