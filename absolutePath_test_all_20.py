from pathlib import Path

# 원본 파일 경로
input_file_path = Path("/home/a/hyu_sang/kaist-rgbt/test-all-20.txt")

# 변경된 내용을 저장할 리스트
modified_paths = []

# 파일 내용 읽기
lines = input_file_path.read_text().splitlines()

# 제거할 경로 부분
part_to_remove = "datasets/kaist-rgbt"

for line in lines:
    # 경로에서 지정된 부분을 제거
    if part_to_remove in line:
        modified_path = line.replace(part_to_remove, "").strip("/")
        # 절대 경로로 변환
        abs_path = str(Path("/" + modified_path).resolve())
        modified_paths.append(abs_path)

# 결과를 원본 파일에 다시 쓰기
input_file_path.write_text("\n".join(modified_paths))

print(f"Updated {input_file_path} with modified paths.")
