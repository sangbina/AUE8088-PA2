import os
import json
from pathlib import Path
import re

# 이미지의 고정 크기 (예: 너비 640, 높이 512)
IMG_WIDTH = 640
IMG_HEIGHT = 512

def extract_image_id(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        raise ValueError(f"No valid image ID found in filename: {filename}")

def convert_predictions_to_custom_json(txt_dir, output_json):
    results = []
    txt_files = list(Path(txt_dir).glob('*.txt'))

    print(f"Found {len(txt_files)} txt files in {txt_dir}")

    for txt_file in txt_files:
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        
        print(f"Processing file: {txt_file}, with {len(lines)} lines")

        image_name = txt_file.stem
        try:
            image_id = extract_image_id(txt_file.stem)
        except ValueError as e:
            print(e)
            continue

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 6:
                print(f"Skipping malformed line: {line}")
                continue  # Skip malformed lines

            try:
                category_id = int(parts[0])
                bbox = [float(x) for x in parts[1:5]]
                confidence = float(parts[5])
            except ValueError as e:
                print(f"Skipping line due to value error: {line}, error: {e}")
                continue

            # YOLO format (center_x, center_y, width, height) to custom format (x_min, y_min, width, height)
            center_x, center_y, width, height = bbox
            x_min = (center_x - width / 2) * IMG_WIDTH
            y_min = (center_y - height / 2) * IMG_HEIGHT
            width *= IMG_WIDTH
            height *= IMG_HEIGHT
            custom_bbox = [x_min, y_min, width, height]

            result = {
                "image_name": image_name,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": custom_bbox,
                "score": confidence
            }
            results.append(result)

    print(f"Writing {len(results)} results to {output_json}")

    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)

# Example usage
txt_dir = 'runs/detect/exp7/labels'  # detect.py 결과 텍스트 파일 경로
output_json = 'predictions_custom.json'
convert_predictions_to_custom_json(txt_dir, output_json)

print(f"Custom formatted predictions saved to {output_json}")
