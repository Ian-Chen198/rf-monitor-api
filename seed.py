"""
seed.py — 建立範例資料，方便測試 API
執行方式：python seed.py
"""
from database import SessionLocal, engine, Base
import models, schemas, crud

Base.metadata.create_all(bind=engine)

EQUIPMENT = [
    schemas.EquipmentCreate(
        name="RGA-3001",
        brand="DAIHEN",
        model="RGA-3000 Series",
        category="RF Generator",
        location="Fab A - Chamber 1",
        status="normal",
        power_output_kw=3.0,
        frequency_mhz=13.56,
    ),
    schemas.EquipmentCreate(
        name="AX-5002",
        brand="ADTEC",
        model="AX Series",
        category="RF Generator",
        location="Fab A - Chamber 2",
        status="warning",
        power_output_kw=5.0,
        frequency_mhz=13.56,
    ),
    schemas.EquipmentCreate(
        name="HV-PS2NC-01",
        brand="KYOSAN",
        model="HV-PS2NC",
        category="HV Power Supply",
        location="Fab B - Station 3",
        status="fault",
        power_output_kw=2.0,
        frequency_mhz=None,
    ),
    schemas.EquipmentCreate(
        name="AMS-6001",
        brand="MAX",
        model="AMS-6KPNX",
        category="RF Generator",
        location="Fab B - Chamber 1",
        status="offline",
        power_output_kw=6.0,
        frequency_mhz=2.45,
    ),
]

LOGS = [
    (1, schemas.LogCreate(action="例行點檢", description="輸出功率穩定，無異常", engineer="陳劭泓", result="success")),
    (1, schemas.LogCreate(action="更換風扇濾網", description="濾網積塵嚴重，清潔更換", engineer="陳劭泓", result="success")),
    (2, schemas.LogCreate(action="輸出功率異常排查", description="功率波動超標，懷疑電容老化，待確認", engineer="陳劭泓", result="pending")),
    (3, schemas.LogCreate(action="更換輸出電容 C102", description="C102漏液導致過壓保護跳機，更換後待上機驗證", engineer="陳劭泓", result="pending")),
    (4, schemas.LogCreate(action="定期保養", description="清潔機台、量測各點電壓正常後下線備用", engineer="陳劭泓", result="success")),
]

def seed():
    db = SessionLocal()
    try:
        existing = db.query(models.Equipment).count()
        if existing > 0:
            print("⚠️  資料庫已有資料，跳過 seed。若要重置請刪除 rf_monitor.db 後重新執行。")
            return

        eq_ids = []
        for payload in EQUIPMENT:
            eq = crud.create_equipment(db, payload)
            eq_ids.append(eq.id)
            print(f"✅ 建立設備：[{eq.id}] {eq.name} ({eq.brand})")

        for eq_id, log_payload in LOGS:
            log = crud.create_log(db, eq_id, log_payload)
            print(f"📋 新增維護紀錄：設備 {eq_id} — {log.action}")

        print("\n🎉 Seed 完成！執行 uvicorn main:app --reload 啟動 API")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
