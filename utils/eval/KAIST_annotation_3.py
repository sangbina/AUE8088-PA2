import json
import os

def generate_kaist_annotation(val_file, labels_dir, output_json_file):
    image_height = 512
    image_width = 640

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

    with open(val_file, 'r') as f:
        lines = f.readlines()

    image_id = 0
    annotation_id = 0

    def read_label_file(label_file_path):
        with open(label_file_path, 'r') as f:
            lines = [line.strip().split() for line in f]
        return lines if lines else None

    for line in lines:
        parts = line.strip().split('/')
        if len(parts) < 2:
            print(f"Warning: Skipping line due to insufficient data: {line.strip()}")
            continue

        image_file_name = parts[-1]
        label_file_name = image_file_name.replace('.jpg', '.txt')
        label_file_path = os.path.join(labels_dir, label_file_name)

        results["images"].append({
            "id": image_id,
            "im_name": image_file_name,
            "height": image_height,
            "width": image_width
        })

        if os.path.exists(label_file_path):
            label_data = read_label_file(label_file_path)

            if label_data:
                for label in label_data:
                    category_id = int(label[0])
                    center_x = float(label[1]) * image_width
                    center_y = float(label[2]) * image_height
                    bbox_width = float(label[3]) * image_width
                    bbox_height = float(label[4]) * image_height

                    x_min = center_x - (bbox_width / 2)
                    y_min = center_y - (bbox_height / 2)
                    bbox = [x_min, y_min, bbox_width, bbox_height]

                    annotation_entry = {
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": bbox,
                        "height": bbox_height,
                        "occlusion": 0,
                        "ignore": 0
                    }
                    results["annotations"].append(annotation_entry)
                    annotation_id += 1
            else:
                print(f"Warning: Label file is empty for image: {image_file_name}")

        else:
            print(f"Warning: Label file not found for image: {image_file_name}")

        image_id += 1

    with open(output_json_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"KAIST_annotation.json has been created at {output_json_file}")

# 평가 스크립트 실행
val_file = 'test-all-20.txt'  # 평가에 사용할 파일
labels_dir = 'train/labels'
output_json_file = '/utils/eval/KAIST_annotation.json'

try:
    # KAIST_annotation.json 파일 생성
    generate_kaist_annotation(val_file, labels_dir, output_json_file)
    pred_json = 'path_to_pred_json_file.json'  # 예측 결과 파일 경로
    os.system(f"python3 kaisteval.py --annFile {output_json_file} --rstFile {pred_json}")
except Exception as e:
    print(f"kaisteval unable to run: {e}")
