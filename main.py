from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import SessionLocal, engine, Base
import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RF Equipment Monitor API",
    description="設備狀態監控系統 — 管理與追蹤射頻設備的即時狀態與維護紀錄",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── 設備 Equipment ──────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {"message": "RF Equipment Monitor API is running 🚀"}


@app.get("/equipment", response_model=List[schemas.EquipmentOut], tags=["Equipment"])
def list_equipment(brand: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    """列出所有設備，可依品牌或狀態過濾"""
    return crud.get_equipment_list(db, brand=brand, status=status)


@app.get("/equipment/{equipment_id}", response_model=schemas.EquipmentOut, tags=["Equipment"])
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """取得單一設備詳細資訊"""
    eq = crud.get_equipment(db, equipment_id)
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return eq


@app.post("/equipment", response_model=schemas.EquipmentOut, status_code=201, tags=["Equipment"])
def create_equipment(payload: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    """新增設備"""
    return crud.create_equipment(db, payload)


@app.patch("/equipment/{equipment_id}/status", response_model=schemas.EquipmentOut, tags=["Equipment"])
def update_status(equipment_id: int, payload: schemas.StatusUpdate, db: Session = Depends(get_db)):
    """更新設備狀態（normal / warning / fault / offline）"""
    eq = crud.update_equipment_status(db, equipment_id, payload.status)
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return eq


@app.delete("/equipment/{equipment_id}", tags=["Equipment"])
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """刪除設備"""
    ok = crud.delete_equipment(db, equipment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return {"detail": "Deleted successfully"}


# ── 維護紀錄 Maintenance Log ────────────────────────────────

@app.get("/equipment/{equipment_id}/logs", response_model=List[schemas.LogOut], tags=["Maintenance Log"])
def list_logs(equipment_id: int, db: Session = Depends(get_db)):
    """取得設備所有維護紀錄"""
    return crud.get_logs(db, equipment_id)


@app.post("/equipment/{equipment_id}/logs", response_model=schemas.LogOut, status_code=201, tags=["Maintenance Log"])
def create_log(equipment_id: int, payload: schemas.LogCreate, db: Session = Depends(get_db)):
    """新增維護紀錄"""
    eq = crud.get_equipment(db, equipment_id)
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return crud.create_log(db, equipment_id, payload)


# ── 統計 Summary ────────────────────────────────────────────

@app.get("/summary", tags=["Summary"])
def summary(db: Session = Depends(get_db)):
    """取得設備狀態統計總覽"""
    return crud.get_summary(db)
