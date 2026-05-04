from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)          # 設備名稱，例如 RGA-3001
    brand = Column(String(50), nullable=False)           # 品牌，例如 DAIHEN
    model = Column(String(50), nullable=False)           # 型號
    category = Column(String(50), default="RF Generator")  # 設備類型
    location = Column(String(100), nullable=False)       # 安裝位置
    status = Column(String(20), default="normal")        # normal / warning / fault / offline
    power_output_kw = Column(Float, nullable=True)       # 額定功率 (kW)
    frequency_mhz = Column(Float, nullable=True)         # 頻率 (MHz)
    installed_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = relationship("MaintenanceLog", back_populates="equipment", cascade="all, delete")


class MaintenanceLog(Base):
    __tablename__ = "maintenance_log"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    action = Column(String(100), nullable=False)         # 維護動作，例如「更換電容」
    description = Column(Text, nullable=True)            # 詳細描述
    engineer = Column(String(50), nullable=False)        # 負責工程師
    result = Column(String(20), default="success")       # success / failed / pending
    logged_at = Column(DateTime, default=datetime.utcnow)

    equipment = relationship("Equipment", back_populates="logs")
