import random

# train-all-19.txt 파일 경로
input_file = 'train-all-19.txt'

# 분할된 train.txt 및 val.txt 파일 경로
train_output_file = 'train.txt'
val_output_file = 'val.txt'

# 파일 읽기
with open(input_file, 'r') as f:
    all_images = f.readlines()

# 데이터 섞기
random.shuffle(all_images)

# 데이터 분할 (80% 훈련 데이터, 20% 검증 데이터)
train_split = int(0.8 * len(all_images))
train_images = all_images[:train_split]
val_images = all_images[train_split:]

# train.txt 파일로 저장
with open(train_output_file, 'w') as f:
    f.writelines(train_images)

# val.txt 파일로 저장
with open(val_output_file, 'w') as f:
    f.writelines(val_images)

print(f"총 {len(all_images)}개의 이미지 중 {len(train_images)}개는 train.txt로, {len(val_images)}개는 val.txt로 저장되었습니다.")
