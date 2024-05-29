# Model
from model import *
import pandas as pd

# API
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# OS File
import glob
import os

# Cấu hình
folder_path = "."
extension = "*.sav"
data_path = "../db/cleaned_data.csv"
non_label_csv = "../db/test_prediction.csv"

os.system("cls")

# Tải model
model_arr = load_model_from_file()

print("=====> API đang chạy ở http://localhost:8000")

# Khởi tạo web server
app = FastAPI()


# Cấu hình CORS
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tổng quan về dataset
@app.get("/api/info")
def models_list():
    df = pd.read_csv(data_path)
    return JSONResponse(
        content=jsonable_encoder(
            {
                "number_of_feature": 100,
                "number_of_sample": 1612,
                "training_sample": 1500,
                "testing_sample": 112,
            }
        )
    )


# Danh sách các model
@app.get("/api/model")
def models_list():
    entries = []
    for item in model_arr:
        entry = item.copy()
        del entry["model"]
        entries.append(entry)
    return JSONResponse(content=jsonable_encoder({"entries": entries}))


# Lấy ngẫu nhiên danh sách từ tập dữ liệu chưa label
@app.get("/api/raw-data")
def models_list():
    raw_dataset = pd.read_csv(non_label_csv)
    sample = raw_dataset.sample(n=5)
    print(sample)
    return JSONResponse(
        content=jsonable_encoder({"entries": sample.to_dict(orient="records")})
    )


# Dự đoán
@app.post("/api/predict")
async def process_data(data: dict):
    print(data)
    result, best_choice, recom_dict = predict(
        data_path, model_arr, data["check_text"].lower()
    )
    return JSONResponse(
        content=jsonable_encoder(
            {"entries": result, "best_choice": best_choice, "recom_dict": recom_dict}
        )
    )
