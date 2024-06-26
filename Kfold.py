import os
from sklearn.model_selection import KFold


# 텍스트 파일 읽기
with open('train-all-04.txt', 'r') as f:
    images = f.readlines()

# 5개의 폴드 생성
kf = KFold(n_splits=5)
folds = list(kf.split(images))
for i, (train_idx, val_idx) in enumerate(folds):
    train_fold = [images[idx] for idx in train_idx]
    val_fold = [images[idx] for idx in val_idx]

    # 해당 폴드의 train 및 val 파일 작성
    with open(f'train_fold{i}.txt', 'w') as f:
        f.writelines(train_fold)
    
    with open(f'val_fold{i}.txt', 'w') as f:
        f.writelines(val_fold)

