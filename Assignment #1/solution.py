import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

def is_leaf_node(node):
    # A node is considered a leaf if it has no child nodes
    return (len(node) == 0)

def process_xml(xml_file, png_file):
    xml_path = os.path.join(data_folder, xml_file)
    png_path = os.path.join(data_folder, png_file)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        img = Image.open(png_path)
        draw = ImageDraw.Draw(img)

        for node in root.iter():
            if is_leaf_node(node):
                bounds = node.get('bounds')
                if bounds:
                    # Split the bounds string and convert to integers
                    coords = [int(x) for x in bounds.strip('[]').replace('][', ',').split(',')]
                    # Draw rectangle using [left, top, right, bottom] format
                    draw.rectangle(coords, outline='yellow', width=10)

        output_folder = 'output'
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, png_file.replace('.png', '_annotated.png'))
        img.save(output_file)
        print(f"Annotated image saved as {output_file}")

    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file}: {e}")

    except Exception as e:
        print(f"Error processing {xml_file} and {png_file}: {e}")

# Process each XML/PNG pair
data_folder = 'data'
xml_files = [f for f in os.listdir(data_folder) if f.endswith('.xml')]
png_files = [f for f in os.listdir(data_folder) if f.endswith('.png')]

for xml_file, png_file in zip(xml_files, png_files):
    process_xml(xml_file, png_file)
