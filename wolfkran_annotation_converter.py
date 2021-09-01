import os
import glob
import logging
from pathlib import Path
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.DEBUG)

DATA_PATH = Path(__file__).absolute().parent / 'build' / 'darknet' / 'x64' / 'data' / 'obj' / 'wolf_data' / 'annotations'
OUTPUT_PATH = Path(__file__).absolute().parent / 'build' / 'darknet' / 'x64' / 'data' / 'obj' / 'wolf_data' / 'yolo_annotations'

# Make the output directory
os.makedirs(OUTPUT_PATH, exist_ok=True)

files = sorted(glob.glob(f'{DATA_PATH}/*.xml'))
for f in files:
    tree = ET.parse(f)
    root = tree.getroot()

    # Get width and height of the image
    width = int(root.find("size/width").text)
    height = int(root.find("size/height").text)
    logging.debug(f"width: {width} | height: {height}")

    # Create an annotation file
    output_file_path = OUTPUT_PATH / Path(f).with_suffix('.txt').name
    print(output_file_path)
    out_file = open(output_file_path, 'w')

    for child in root.findall('object'):
        obj_type = child.find('name').text
        if obj_type == "person":
            # Convert pixel values of the bounding box to float [0.0 - 1.0]
            xmin = int(child.find('bndbox/xmin').text) / width
            ymin = int(child.find('bndbox/ymin').text) / height
            xmax = int(child.find('bndbox/xmax').text) / width
            ymax = int(child.find('bndbox/ymax').text) / height

            # Find the center, width and height of each box (relative to width and height)
            relwidth = xmax - xmin
            relheight = ymax - ymin
            xcenter = xmin + relwidth / 2
            ycenter = ymin + relheight / 2

            logging.debug(f'xmin: {xmin:.3f} | ymin: {ymin:.3f} | xmax: {xmax:.3f} | ymax: {ymax:.3f} || relwidth: {relwidth:.3f} | relheight: {relheight:.3f} | xcenter: {xcenter:.3f} | ycenter: {ycenter:.3f}')

            # Add the annotated object in the darknet format
            annot_str = f'0 {xcenter} {ycenter} {relwidth} {relheight}\n'
            out_file.write(annot_str)
    out_file.close()
