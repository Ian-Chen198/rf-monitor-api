# RF Equipment Monitor API

> 射頻設備狀態監控系統 — 以 FastAPI 建構的 RESTful API，用於管理與追蹤工廠射頻（RF）設備的即時狀態與維護紀錄。

---

**🚀 Live Demo：https://rf-monitor-api-833520519375.asia-east1.run.app/docs**

---

## 專案背景

本專案源自本人在半導體/塑膠製品製造業擔任設備維護工程師近三年的實務經驗。  
日常負責維護 DAIHEN RGA、ADTEC AX、KYOSAN HV-PS2NC、MAX AMS-6KPNX 等多品牌射頻產生器與高壓電源供應器。  
傳統上設備狀態與維護紀錄仰賴紙本或 Excel，本專案旨在以標準化 API 取代人工記錄流程，作為工廠設備管理數位化的後端基礎。

---

## 技術架構

| 層次 | 技術 |
|------|------|
| Web Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| 資料驗證 | Pydantic v2 |
| 資料庫 | SQLite（可替換為 PostgreSQL） |
| 伺服器 | Uvicorn |

---

## 功能特色

- ✅ 設備 CRUD（新增、查詢、狀態更新、刪除）
- ✅ 依品牌／狀態過濾設備清單
- ✅ 維護紀錄管理（每次維修動作、負責工程師、結果）
- ✅ 統計總覽（各狀態數量、品牌分布、最近五筆維護）
- ✅ 自動產生互動式 API 文件（Swagger UI）

### 設備狀態定義

| 狀態 | 說明 |
|------|------|
| `normal` | 運作正常 |
| `warning` | 異常警示，需關注 |
| `fault` | 故障，停機維修中 |
| `offline` | 下線／備用 |

---

## 快速開始

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 建立範例資料

```bash
python seed.py
```

### 3. 啟動 API 伺服器

```bash
uvicorn main:app --reload
```

伺服器啟動後開啟瀏覽器：

- **Swagger UI（互動文件）**：http://127.0.0.1:8000/docs
- **ReDoc**：http://127.0.0.1:8000/redoc

---

## API 端點總覽

### Equipment（設備）

| Method | Endpoint | 說明 |
|--------|----------|------|
| `GET` | `/equipment` | 列出所有設備（支援 `?brand=DAIHEN&status=normal` 過濾） |
| `GET` | `/equipment/{id}` | 取得單一設備詳情 |
| `POST` | `/equipment` | 新增設備 |
| `PATCH` | `/equipment/{id}/status` | 更新設備狀態 |
| `DELETE` | `/equipment/{id}` | 刪除設備 |

### Maintenance Log（維護紀錄）

| Method | Endpoint | 說明 |
|--------|----------|------|
| `GET` | `/equipment/{id}/logs` | 取得設備所有維護紀錄 |
| `POST` | `/equipment/{id}/logs` | 新增維護紀錄 |

### Summary（統計）

| Method | Endpoint | 說明 |
|--------|----------|------|
| `GET` | `/summary` | 設備狀態統計總覽 |

---

## 使用範例

### 新增設備

```bash
curl -X POST http://127.0.0.1:8000/equipment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RGA-3001",
    "brand": "DAIHEN",
    "model": "RGA-3000 Series",
    "category": "RF Generator",
    "location": "Fab A - Chamber 1",
    "status": "normal",
    "power_output_kw": 3.0,
    "frequency_mhz": 13.56
  }'
```

### 更新設備狀態

```bash
curl -X PATCH http://127.0.0.1:8000/equipment/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "fault"}'
```

### 新增維護紀錄

```bash
curl -X POST http://127.0.0.1:8000/equipment/1/logs \
  -H "Content-Type: application/json" \
  -d '{
    "action": "更換輸出電容 C102",
    "description": "C102 漏液導致過壓保護跳機，更換同規格元件後輸出恢復正常",
    "engineer": "陳劭泓",
    "result": "success"
  }'
```

### 查詢統計

```bash
curl http://127.0.0.1:8000/summary
```

---

## 專案結構

```
rf-monitor-api/
├── main.py          # FastAPI 應用程式與路由
├── models.py        # SQLAlchemy 資料庫模型
├── schemas.py       # Pydantic 資料驗證 Schema
├── crud.py          # 資料庫操作邏輯
├── database.py      # 資料庫連線設定
├── seed.py          # 範例資料建立腳本
├── requirements.txt
└── README.md
```

---

## 未來規劃

- [ ] 加入 JWT 身份驗證
- [ ] 切換至 PostgreSQL
- [ ] 新增設備功率趨勢記錄與異常告警
- [ ] Docker 容器化部署
- [ ] 串接前端儀表板

---

## 作者

**陳劭泓 (CHEN, SHAO-HUNG)**  
東海大學 資訊管理學系 碩士  
設備維護工程師 / 維運工程師候選人  
[ian870604@gmail.com](mailto:ian870604@gmail.com)
