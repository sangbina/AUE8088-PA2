import json
import os

# val.txt 파일 경로
val_file = 'val.txt'

# 라벨 파일이 저장된 디렉토리 경로
labels_dir = 'train/labels'

# JSON 파일로 저장할 경로
output_json_file = 'KAIST_annotation.json'

# 이미지 크기 고정값
image_height = 512
image_width = 640

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

# 라벨 파일 읽기 함수 정의
def read_label_file(label_file_path):
    with open(label_file_path, 'r') as f:
        lines = [line.strip().split() for line in f]
    return lines if lines else None  # 비어 있는 경우 None 반환

# val.txt 내용을 JSON 구조로 변환
for line in lines:
    # {} 부분을 lwir 및 visible로 대체하여 경로 생성
    lwir_path = line.strip().format('lwir')
    visible_path = line.strip().format('visible')

    # 파일 이름 추출
    image_file_name = lwir_path.split('/')[-1]  # 'set04_V000_I02011.jpg'
    label_file_name = image_file_name.replace('.jpg', '.txt')
    label_file_path = os.path.join(labels_dir, label_file_name)

    # 이미지 정보 추가
    results["images"].append({
        "id": image_id,
        "im_name": image_file_name,
        "height": image_height,  # 고정된 이미지 높이
        "width": image_width    # 고정된 이미지 너비
    })

    # 라벨 파일이 존재하는지 확인
    if os.path.exists(label_file_path):
        label_data = read_label_file(label_file_path)

        if label_data:  # 라벨 데이터가 비어 있지 않은 경우
            for label in label_data:
                category_id = int(label[0])
                center_x = float(label[1]) * image_width
                center_y = float(label[2]) * image_height
                bbox_width = float(label[3]) * image_width
                bbox_height = float(label[4]) * image_height

                # COCO 형식의 bbox는 [x_min, y_min, width, height] 형식
                x_min = center_x - (bbox_width / 2)
                y_min = center_y - (bbox_height / 2)
                bbox = [x_min, y_min, bbox_width, bbox_height]

                annotation_entry = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "bbox": bbox,
                    "height": bbox_height,  # bbox의 높이 값 사용
                    "occlusion": 0,  # 기본값 0
                    "ignore": 0  # 기본값 0
                }
                results["annotations"].append(annotation_entry)
                annotation_id += 1
        else:
            print(f"Warning: Label file is empty for image: {image_file_name}")

    else:
        print(f"Warning: Label file not found for image: {image_file_name}")

    image_id += 1

# JSON 파일로 저장
with open(output_json_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"결과가 {output_json_file}에 저장되었습니다.")
