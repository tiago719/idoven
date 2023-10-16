from fastapi import Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated, List
from middleware.authentication import get_current_user
from models.ecg import ECG, Lead
from models.user import User
from database import get_db
from routers import router


class LeadCreate(BaseModel):
    name: str
    signal: list[int]


class ECGCreate(BaseModel):
    leads: List[LeadCreate]


class ECGResponse(BaseModel):
    id: int
    date: str
    leads: List[LeadCreate]


@router.post("/ecgs", response_model=ECGResponse)
def create_ecg(
    ecg_data: ECGCreate,
    background_tasks: BackgroundTasks,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # Create an ECG instance and associate it with the user
    ecg = ECG(user=user.id)
    db.add(ecg)
    db.commit()
    db.refresh(ecg)

    # Create Lead instances and associate them with the ECG
    leads = []
    for lead_data in ecg_data.leads:
        lead = Lead(ecg=ecg, name=lead_data.name, signal=lead_data.signal)
        leads.append(lead)
    db.add_all(leads)
    db.commit()
    
    background_tasks.add_task(calculate_ecg_insights, ecg, db)
    return ECGResponse(
        id=ecg.id,
        date=str(ecg.date),
        leads=[{"name": lead.name, "signal": lead.signal} for lead in leads])


class Insights(BaseModel):
    zero_crossings: int


@router.get("/ecgs/{ecg_id}/insights", response_model=Insights)
def get_ecg_insights(
    ecg_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ecg = db.query(ECG).filter(ECG.id == ecg_id, ECG.user == user.id).first()
    if ecg:
        if ecg.processed:
            return {"zero_crossings": ecg.zero_crossings}
        else:
            raise HTTPException(status_code=400, detail="not processed")
    raise HTTPException(status_code=404, detail="ECG not found")


def calculate_ecg_insights(ecg: ECG, db: Session):
    zero_crossings = 0
    for lead in ecg.leads:
        zero_crossings += calculate_zero_crossings(lead.signal)
    ecg.zero_crossings = zero_crossings
    ecg.processed = True

    db.commit()


def calculate_zero_crossings(signal):
    zero_crossings = 0
    for i in range(1, len(signal)):
        if (signal[i - 1] > 0 and signal[i] < 0) or (signal[i - 1] < 0 and signal[i] > 0):
            zero_crossings += 1
    return zero_crossings
