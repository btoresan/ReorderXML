import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import argparse


"""
Attempts to correctly order the items in a vgt extraction file
This is done by grouping the items by the x coordinates position (distance bellow threshold)
Then each group is ordered by their y0 component
"""

class FileOrganizer:
    #Parsed the xml file and writes the items in order
    @staticmethod
    def organizeFile(path_input, path_output):
        tree = ET.parse(path_input)
        root = tree.getroot()
        
        for i, page in enumerate(root.findall(".//page")):
               FileOrganizer._organizePage(page, i)

        with open(path_output, 'w', encoding='utf-8') as f:
            f.write(FileOrganizer.pretty_print_xml(tree))
    
    #Organizes all items in a page first from right to left
    #then from top to bottom (origin (0,0) is at the bottom left of the page)
    @staticmethod
    def _organizePage(page, i):
        items = page.findall(".//item")
        if len(items) > 1:
            sorted_items = FileOrganizer._organizeItemsTopologically(items)
            
            page.clear()
            page.set("number", str(i))
            
            for item in sorted_items:
                page.append(item)
            
    #Topological logic to order the items of a page
    @staticmethod
    def _organizeItemsTopologically(items, std_multiplier=0.9):
        #Sorts the items by their x0 coordinates and saves the distances between neighbors
        items = sorted(items, key=lambda item: (int(item.get('x0'))))
        
        distances = []
        for i in range(len(items) - 1):
            distances.append(int(items[i+1].get('x0')) - int(items[i].get('x0')))
            
        #Calculates the threshold based on the mean and standard deviation of the distances
        avg_distance = np.mean(distances)
        std_dev_distance = np.std(distances)
        threshold = avg_distance + std_multiplier*std_dev_distance
        
        sorted_items = []
        item_group = [items[0]]

        #Organizes the items into groups where a group of items are within a threshold distance from each other
        #Groups are sorted internally by y1
        for i in range(1, len(items)):
            if distances[i-1] > threshold:
                sorted_items.extend(FileOrganizer._organizeItemGroup(item_group))
                item_group = [items[i]]
            else:
                item_group.append(items[i])
 
        # Adds any remaining items in the last group      
        sorted_items.extend(FileOrganizer._organizeItemGroup(item_group))
        
        for i, item in enumerate(sorted_items):
            item.set("block", str(i))
                
        return sorted_items
    
    #ORganizes a group of items by their vertical coordinate
    @staticmethod
    def _organizeItemGroup(item_group):
        return sorted(item_group, key=lambda item: (int(item.get('y0'))))
    
    @staticmethod
    def pretty_print_xml(tree):
        #Convert the tree to a nicely formatted string with indentation
        rough_string = ET.tostring(tree.getroot(), 'utf-8')
        reparse = minidom.parseString(rough_string)
        return reparse.toprettyxml(indent="  ")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Duplicate xml organizing items by order (hopefully)")
    parser.add_argument("input_path", help="Path to the input XML file")
    parser.add_argument("output_path", help="Path to the output XML file")
    
    args = parser.parse_args()
    
    FileOrganizer.organizeFile(args.input_path, args.output_path)