import pandas as pd
from pandas.errors import SettingWithCopyWarning
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.simplefilter("ignore", category=SettingWithCopyWarning)
import pickle
import os
import string
from collections import Counter


def load_model_from_file():
    paths = [
        "BestAccuracyModel",
        "SVM-Kernel-RBF",
        "KNeighborsClassifier",
        "LogisticRegression",
        "GradientBoostingClassifier",
        "MultinomialNB",
        "RandomForestClassifier",
        "DecisionTreeClassifier",
    ]
    models = []
    main_file_path = os.path.abspath(__file__)
    main_dir = os.path.dirname(main_file_path)
    for path in paths:
        filename = os.path.join(main_dir, path + ".sav")
        if os.path.exists(filename):
            model = pickle.load(open(filename, "rb"))
            models.append({"name": path, "model": model})
            print("Da tai thanh cong model", path)
        else:
            print("khong tim thay file file", path)
    return models


def predict(data_path, models, check_text):
    import string
    from underthesea import (
        word_tokenize,
    )  # Thư viện xử lý ngôn ngữ tự nhiên cho tiếng Việt

    with open("./vietnamese_stopwords.txt", "r", encoding="utf-8") as f:
        vietnamese_stopwords = set(f.read().splitlines())
    punctuations = string.punctuation

    check_text = "".join(ch for ch in check_text if ch not in punctuations)
    words = word_tokenize(check_text.lower())
    words = [word for word in words if word not in vietnamese_stopwords]
    check_text = " ".join(words)
    print(check_text)

    # Trích xuất đặc trưng
    with open("count_vectorizer.pkl", "rb") as f:
        loaded_cv = pickle.load(f)

    original_classes = [
        "Công nghệ",
        "Kinh doanh và khởi nghiệp",
        "Kỹ năng",
        "Marketing",
        "Ngoại ngữ",
        "Phong cách sống",
        "Sales bán hàng",
        "Sức khỏe và làm đẹp",
        "Thiết kế và xây dựng",
        "Tin học văn phòng",
        "Tài chính và kế toán",
        "Tình yêu, hôn nhân và gia đình",
    ]

    check_text = loaded_cv.transform([check_text])
    print(check_text)
    # Dự đoán và xử lý dữ liệu trả về
    result = []
    predictions = []
    for item in models:
        model = item["model"]
        prediction = model.predict(check_text)
        prediction = original_classes[prediction[0]]
        predictions.append(prediction)
        result.append({"name": item["name"], "prediction": prediction})
    print(result)

    best_choice = predictions[0]
    raw_df = pd.read_csv(data_path)
    recom_dict = (
        raw_df[raw_df["category"] == best_choice]
        .sort_values(
            by=["average_rating", "review_count", "students_enrolled"],
            ascending=[False, False, True],
        )
        .head(10)
        .to_dict(orient="records")
    )
    return result, best_choice, recom_dict
