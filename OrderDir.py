import os, argparse
from  ReOrder import FileOrganizer
from tqdm import tqdm
import logging

"""
Reorders the items of all the xml files inside a dir
the new xml files are saved in the output dir
the old xml are not modified
"""

parser = argparse.ArgumentParser(description="Duplicate and reorder all the xmls in a dir to a new dir(hopefully)")
parser.add_argument("input_path", help="Path to the input dir")
parser.add_argument("output_path", help="Path to the output dir")

args = parser.parse_args()

for file in tqdm(os.listdir(args.input_path)):
    if file.endswith(".xml"):
        try:    
            FileOrganizer.organizeFile(f"{args.input_path}/{file}", f"{args.output_path}/{file}")
        except Exception as e:
            print(f"An error occrued: {e}")
            logging.error(f"An error occrued: {e}")