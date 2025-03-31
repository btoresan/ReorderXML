import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os, argparse

"""
Draws the bounding boxes of the xml from vgt extraction
(0,0) is upper left corner
"""

# Function to parse XML and extract coordinates for each page
def parse_xml_from_file(file_path):
    tree = ET.parse(file_path)  
    root = tree.getroot()  
    pages = []

    for page in root.findall('page'):  # Find all <page> elements
        boxes = []
        for item in page.findall('item'):  # Find all <item> elements in the current page
            x0 = float(item.get('x0'))
            x1 = float(item.get('x1'))
            y0 = float(item.get('y0'))
            y1 = float(item.get('y1'))
            boxes.append((x0, y0, x1, y1))  # Store the box coordinates for the current page
        pages.append(boxes)
    
    return pages

# Function to visualize the boxes and save the plot for each page
def visualize_and_save_boxes(boxes, output_dir, file_name):
    fig, ax = plt.subplots()

    for box in boxes:
        x0, y0, x1, y1 = box
        width = x1 - x0
        height = y1 - y0
        rect = patches.Rectangle((x0, y0), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    ax.set_xlim(0, 3000)  
    ax.set_ylim(3000, 0)   
    ax.set_aspect('equal', 'box')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the figure to the output directory
    output_path = os.path.join(output_dir, file_name)
    plt.savefig(output_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Draw bounding boxes from XML and save images")
    parser.add_argument("input_file", help="Path to the input xml")
    parser.add_argument("output_path", help="Path to the output dir")

    args = parser.parse_args()

    file_path =  args.input_file 
    output_dir = args.output_path 
    
    # Parse the XML and extract the box coordinates for all pages
    pages = parse_xml_from_file(file_path)
    
    # Loop through all pages and save each one as a separate image
    for page_idx, boxes in enumerate(pages):
        file_name = f"page_{page_idx + 1}.png" 
        visualize_and_save_boxes(boxes, output_dir, file_name)


if __name__ == "__main__":
    main()
