import os
import subprocess

# 경로 설정
dataset_path = 'datasets/kaist-rgbt'

# 클래스 이름 설정
class_names = ["person", "cyclist", "people", "person?"]

# 각 폴드에 대해 훈련 실행
for fold in range(5):
    # data.yaml 파일 생성
    data_yaml_path = f"{dataset_path}/data_fold{fold}.yaml"
    with open(data_yaml_path, 'w') as f:
        f.write(f"path: {dataset_path}\n")
        f.write(f"train: train_fold{fold}.txt\n")
        f.write(f"val: val_fold{fold}.txt\n")
        f.write("test: test-all-20.txt\n")
        f.write("nc: 4\n")  # number of classes
        f.write(f"names: {class_names}\n")
    # 훈련 실행
    command = [
        "python", "train_simple.py",
        "--img", "640",
        "--batch-size", "16",
        "--epochs", "20",
        "--data", data_yaml_path,
        "--cfg", "models/yolov5n_kaist-rgbt.yaml",
        "--weights", "yolov5n.pt",
        "--workers", "16",
        "--name", f"yolov5n-rgbt-fold{fold}",
        "--rgbt",
        "--single-cls"
    ]
    subprocess.run(command)
