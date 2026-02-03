import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_FILE = "database.json"

# 定義 31 個欄位的資料模型
class ProjectItem(BaseModel):
    # --- 專案基本資料 ---
    project_def: Optional[str] = ""       # A: Project definition
    year: Optional[int] = 2024            # B: 年度
    project_name: Optional[str] = ""      # C: 專案名稱
    case_type: Optional[str] = ""         # D: 案件類型
    
    # --- 日期與時程 ---
    start_date: Optional[str] = ""        # E: 開工日
    act_end_date: Optional[str] = ""      # F: 實際完工日期
    est_end_date: Optional[str] = ""      # G: 預計完工日期
    act_days: Optional[float] = 0         # H: 實際施作日數
    est_days: Optional[float] = 0         # I: 預估施作日數
    
    # --- 人力與管理成本 ---
    act_labor_cost: Optional[float] = 0   # J: 實際人力成本
    est_labor_cost: Optional[float] = 0   # K: 預估人力成本
    saved_labor_cost: Optional[float] = 0 # L: 節省人力成本 (未來自動計算)
    labor_opt_rate: Optional[float] = 0   # M: 人力優化比例 (未來自動計算)
    
    est_mgmt_cost: Optional[float] = 0    # N: 預估管理成本
    act_mgmt_cost: Optional[float] = 0    # O: 實際管理成本
    saved_mgmt_cost: Optional[float] = 0  # P: 節省管理成本 (未來自動計算)
    
    # --- 總體成本與利潤 ---
    plan_costs: Optional[float] = 0       # Q: Plan costs
    act_costs: Optional[float] = 0        # R: Act.costs
    profit_opt_rate: Optional[float] = 0  # S: 利潤率優化
    
    # --- 環境貢獻 (預估) ---
    est_carbon_save: Optional[float] = 0  # T: 預估減碳量
    est_elec_save: Optional[float] = 0    # U: 預估節電量
    est_elec_bill_save: Optional[float] = 0 # V: 預估節省電費
    
    # --- 環境貢獻 (實際) ---
    act_carbon_save: Optional[float] = 0  # W: 實際減碳量
    act_elec_save: Optional[float] = 0    # X: 實際節電量
    act_elec_bill_save: Optional[float] = 0 # Y: 實際節省電費
    
    est_water_save: Optional[float] = 0   # Z: 預估節水量
    act_water_save: Optional[float] = 0   # AA: 實際節水量
    
    # --- 碳權 ---
    est_carbon_credit: Optional[float] = 0 # AB: 預估碳權額度
    act_carbon_credit: Optional[float] = 0 # AC: 實際碳權額度
    est_carbon_value: Optional[float] = 0  # AD: 預估碳權價值
    act_carbon_price: Optional[float] = 0  # AE: 實際碳權現價

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

# 這次我們改為「接收整張表」並覆蓋儲存 (適合 Excel 模式)
@app.post("/save_all")
def save_all(items: List[ProjectItem]):
    data = [item.dict() for item in items]
    save_db(data)
    return {"message": "全表儲存成功", "count": len(data)}

@app.get("/get_projects")
def get_projects():
    return load_db()
