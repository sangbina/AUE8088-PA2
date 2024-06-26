import os

def create_valid_paths(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    valid_paths = []
    for line in lines:
        line = line.strip()
        lwir_path = line.format('lwir')
        visible_path = line.format('visible')
        
        if os.path.exists(lwir_path):
            valid_paths.append(lwir_path)
        elif os.path.exists(visible_path):
            valid_paths.append(visible_path)
        else:
            print(f"Warning: Neither path exists: {lwir_path} nor {visible_path}")

    if not valid_paths:
        raise FileNotFoundError("No valid paths found in both lwir and visible directories.")

    with open(output_file, 'w') as f:
        for path in valid_paths:
            f.write(f"{path}\n")

input_file = 'datasets/kaist-rgbt/test-all-20.txt'
output_file = 'datasets/kaist-rgbt/valid_test_all_20.txt'
create_valid_paths(input_file, output_file)

print(f"Valid paths written to {output_file}")

