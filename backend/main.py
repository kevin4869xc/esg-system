import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # 新增這行
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 允許跨域 (上線後其實可以改更嚴格，但目前先保留)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_FILE = "database.json"

# --- 資料模型 (維持您原本的設定) ---
class ProjectItem(BaseModel):
    project_def: Optional[str] = ""
    year: Optional[int] = 2024
    project_name: Optional[str] = ""
    case_type: Optional[str] = ""
    start_date: Optional[str] = ""
    act_end_date: Optional[str] = ""
    est_end_date: Optional[str] = ""
    act_days: Optional[float] = 0
    est_days: Optional[float] = 0
    act_labor_cost: Optional[float] = 0
    est_labor_cost: Optional[float] = 0
    saved_labor_cost: Optional[float] = 0
    labor_opt_rate: Optional[float] = 0
    est_mgmt_cost: Optional[float] = 0
    act_mgmt_cost: Optional[float] = 0
    saved_mgmt_cost: Optional[float] = 0
    plan_costs: Optional[float] = 0
    act_costs: Optional[float] = 0
    profit_opt_rate: Optional[float] = 0
    est_carbon_save: Optional[float] = 0
    est_elec_save: Optional[float] = 0
    est_elec_bill_save: Optional[float] = 0
    act_carbon_save: Optional[float] = 0
    act_elec_save: Optional[float] = 0
    act_elec_bill_save: Optional[float] = 0
    est_water_save: Optional[float] = 0
    act_water_save: Optional[float] = 0
    est_carbon_credit: Optional[float] = 0
    act_carbon_credit: Optional[float] = 0
    est_carbon_value: Optional[float] = 0
    act_carbon_price: Optional[float] = 0

def load_db():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_db(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.post("/save_all")
def save_all(items: List[ProjectItem]):
    data = [item.dict() for item in items]
    save_db(data)
    return {"message": "全表儲存成功", "count": len(data)}

@app.get("/get_projects")
def get_projects():
    return load_db()

# --- ★★★ 新增：讓後端可以直接顯示 HTML 網頁 ★★★ ---
# 這裡假設您的目錄結構是 project_esg_system 資料夾下有 backend 和 frontend
# Render 執行時通常會在根目錄
import os

# 取得目前檔案的上一層目錄 (即 project_esg_system)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# 掛載前端目錄，讓瀏覽器可以直接存取 html, js, png
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
