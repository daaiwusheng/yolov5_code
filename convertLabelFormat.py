import json
import os

# 转换成class，x , y ,w,h, x1 ,y1, x2, y2, x3, y3, x4, y4这种格式

def convert_to_yolo_format(json_file, output_dir):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    image_path = data['imagePath']
    image_name = os.path.splitext(os.path.basename(image_path.replace("\\", "/")))[0]  # Ensure Linux path format
    txt_file_name = f"{image_name}.txt"

    image_width = data['imageWidth']
    image_height = data['imageHeight']

    yolo_lines = []

    for shape in data['shapes']:
        label = shape['label']
        if label == "pedal":
            points = shape['points']
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]

            # Calculate bounding box
            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)

            bbox_width = x_max - x_min
            bbox_height = y_max - y_min

            x_center = x_min + (bbox_width / 2.0)
            y_center = y_min + (bbox_height / 2.0)

            # Normalize the coordinates
            x_center /= image_width
            y_center /= image_height
            bbox_width /= image_width
            bbox_height /= image_height

            # Normalize the points
            normalized_points = [(x / image_width, y / image_height) for x, y in points]

            # YOLO class index for "pedal" (assuming it's 0)
            yolo_class = 0

            # Generate the line in the required format
            yolo_line = f"{yolo_class} {x_center} {y_center} {bbox_width} {bbox_height}"
            for p in normalized_points:
                yolo_line += f" {p[0]} {p[1]}"

            yolo_lines.append(yolo_line)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Full path to output .txt file
    output_txt_path = os.path.join(output_dir, txt_file_name)

    # Write to output .txt file
    with open(output_txt_path, 'w') as f:
        for line in yolo_lines:
            f.write(line + "\n")

    print(f"YOLO labels saved to {output_txt_path}")


def process_json_files_in_directory(directory, output_dir):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_file_path = os.path.join(root, file)
                convert_to_yolo_format(json_file_path, output_dir)

    print(f"All JSON files in {directory} have been processed and converted.")


if __name__ == "__main__":
    # Example usage
    input_directory = '/home/wangyu/tmp_data/视觉算法测试题/elevator_data/labels'
    output_directory = '/home/wangyu/tmp_data/视觉算法测试题/elevator_data/yolo_labels'
    process_json_files_in_directory(input_directory, output_directory)

    # convert_to_yolo_format('/home/wangyu/tmp_data/视觉算法测试题/1_24_test.json','/home/wangyu/tmp_data/视觉算法测试题/')
