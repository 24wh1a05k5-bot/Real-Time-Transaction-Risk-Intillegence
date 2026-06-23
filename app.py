from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_risk

app = FastAPI()

class Transaction(BaseModel):
    amount: float
    frequency: int

class ResponseModel(BaseModel):
    risk_score: float
    decision: str


@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}


@app.post("/predict", response_model=ResponseModel)
def predict(txn: Transaction):
    risk, reasons = predict_risk(txn.amount, txn.frequency)

    decision = "APPROVE"
    if risk > 0.7:
        decision = "BLOCK"
    elif risk > 0.4:
        decision = "REVIEW"

    return {
        "risk_score": round(risk, 3),
        "decision": decision,
        "reasons": reasons
    }

from typing import List

class ResponseModel(BaseModel):
    risk_score: float
    decision: str
    reasons: List[str]