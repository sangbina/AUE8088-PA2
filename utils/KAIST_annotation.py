import json
import os

# val.txt 파일 경로
val_file = 'val.txt'

# JSON 파일로 저장할 경로
output_json_file = 'KAIST_annotation.json'

# JSON 구조 초기화
results = {
    "info": {
        "dataset": "KAIST Multispectral Pedestrian Benchmark",
        "url": "https://soonminhwang.github.io/rgbt-ped-detection/",
        "related_project_url": "http://multispectral.kaist.ac.kr",
        "publish": "CVPR 2015"
    },
    "info_improved": {
        "sanitized_annotation": {
            "publish": "BMVC 2018",
            "url": "https://li-chengyang.github.io/home/MSDS-RCNN/",
            "target": "files in train-all-02.txt (set00-set05)"
        },
        "improved_annotation": {
            "url": "https://github.com/denny1108/multispectral-pedestrian-py-faster-rcnn",
            "publish": "BMVC 2016",
            "target": "files in test-all-20.txt (set06-set11)"
        }
    },
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 0, "name": "person"},
        {"id": 1, "name": "cyclist"},
        {"id": 2, "name": "people"},
        {"id": 3, "name": "person?"}
    ]
}

# val.txt 파일 읽기
with open(val_file, 'r') as f:
    lines = f.readlines()

# 이미지 ID와 어노테이션 ID 초기화
image_id = 0
annotation_id = 0

# val.txt 내용을 JSON 구조로 변환
for line in lines:
    parts = line.strip().split('/')
    if len(parts) < 2:
        print(f"Warning: Skipping line due to insufficient data: {line.strip()}")
        continue

    image_path = '/'.join(parts[-3:])  # 'set00_V001_I01491.jpg'
    dataset_path = '/'.join(parts[:-3])  # 'datasets/kaist-rgbt/train/images'
    category_id = 0  # 예시에서는 0으로 설정, 실제 데이터에 맞게 수정 필요

    # 이미지 정보 추가
    results["images"].append({
        "id": image_id,
        "im_name": image_path,
        "height": 512,  # 실제 이미지 높이로 수정
        "width": 640    # 실제 이미지 너비로 수정
    })

    # 어노테이션 정보 추가
    results["annotations"].append({
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": [0, 0, 0, 0],  # 실제 바운딩 박스 좌표로 수정 필요
        "height": 0,  # 실제 바운딩 박스 높이로 수정 필요
        "occlusion": 0,
        "ignore": 0
    })

    image_id += 1
    annotation_id += 1

# JSON 파일로 저장
with open(output_json_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"결과가 {output_json_file}에 저장되었습니다.")

