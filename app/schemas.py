from pydantic import BaseModel, Field

class InputData(BaseModel):
    crim: float = Field(ge=0, description="Per capita crime rate (must be >= 0)")
    zn: float = Field(ge=0, description="Proportion of residential land zoned for lots over 25,000 sq.ft.")
    indus: float = Field(ge=0, description="Proportion of non-retail business acres")
    chas: int = Field(ge=0, le=1, description="Charles River dummy variable (0 or 1)")
    nox: float = Field(gt=0, description="Nitric oxides concentration (must be positive)")
    rm: float = Field(gt=0, description="Average number of rooms must be positive")
    age: float = Field(ge=0, description="Proportion of owner-occupied units built prior to 1940")
    dis: float = Field(gt=0, description="Weighted distances to employment centers (must be > 0)")
    rad: int = Field(ge=1, description="Index of accessibility to radial highways (must be >= 1)")
    tax: float = Field(gt=0, description="Full-value property-tax rate (must be > 0)")
    ptratio: float = Field(gt=0, description="Pupil-teacher ratio (must be > 0)")
    b: float = Field(ge=0, description="1000(Bk - 0.63)^2, must be >= 0")
    lstat: float = Field(ge=0, description="% lower status of population, must be >= 0")

class Metadata(BaseModel):
    app_version: str
    model_version: str
    timestamp_utc: str

class PredictResponse(BaseModel):
    prediction: float
    metadata: Metadata
