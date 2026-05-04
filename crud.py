from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

import models, schemas


# ── Equipment ──────────────────────────────────────────────

def get_equipment(db: Session, equipment_id: int):
    return db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()


def get_equipment_list(db: Session, brand: Optional[str] = None, status: Optional[str] = None):
    query = db.query(models.Equipment)
    if brand:
        query = query.filter(models.Equipment.brand.ilike(f"%{brand}%"))
    if status:
        query = query.filter(models.Equipment.status == status)
    return query.order_by(models.Equipment.id).all()


def create_equipment(db: Session, payload: schemas.EquipmentCreate):
    eq = models.Equipment(**payload.model_dump())
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return eq


def update_equipment_status(db: Session, equipment_id: int, status: str):
    eq = get_equipment(db, equipment_id)
    if not eq:
        return None
    eq.status = status
    eq.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(eq)
    return eq


def delete_equipment(db: Session, equipment_id: int):
    eq = get_equipment(db, equipment_id)
    if not eq:
        return False
    db.delete(eq)
    db.commit()
    return True


# ── Maintenance Log ────────────────────────────────────────

def get_logs(db: Session, equipment_id: int):
    return (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.equipment_id == equipment_id)
        .order_by(models.MaintenanceLog.logged_at.desc())
        .all()
    )


def create_log(db: Session, equipment_id: int, payload: schemas.LogCreate):
    log = models.MaintenanceLog(equipment_id=equipment_id, **payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


# ── Summary ────────────────────────────────────────────────

def get_summary(db: Session):
    total = db.query(func.count(models.Equipment.id)).scalar()
    by_status = (
        db.query(models.Equipment.status, func.count(models.Equipment.id))
        .group_by(models.Equipment.status)
        .all()
    )
    by_brand = (
        db.query(models.Equipment.brand, func.count(models.Equipment.id))
        .group_by(models.Equipment.brand)
        .all()
    )
    recent_logs = (
        db.query(models.MaintenanceLog)
        .order_by(models.MaintenanceLog.logged_at.desc())
        .limit(5)
        .all()
    )
    return {
        "total_equipment": total,
        "status_breakdown": {s: c for s, c in by_status},
        "brand_breakdown": {b: c for b, c in by_brand},
        "recent_maintenance": [
            {
                "id": log.id,
                "equipment_id": log.equipment_id,
                "action": log.action,
                "engineer": log.engineer,
                "result": log.result,
                "logged_at": log.logged_at.isoformat(),
            }
            for log in recent_logs
        ],
    }
