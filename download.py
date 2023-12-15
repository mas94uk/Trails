#!/usr/bin/env python3

"""
Download images and construct data directory for a trail.
"""

OUTPUT_ROOT = "trails"
MAX_RESULTS = 5 # Maximum results for each search term
THUMNAIL_SIZE = 200

import glob
import logging
import os
import shutil
import tempfile
from PIL import Image

# Use Bing, as it works better than Google at time of writing
from icrawler.builtin import BingImageCrawler

def combine_images(image_files, item_size, space):
    num_items = len(image_files)
    background_width = int(item_size*num_items + (space*num_items)-space)
    background_height = int(item_size)
    print(f"w {background_width}, h {background_height}")
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 0))

    x = 0
    for i, image_file in enumerate(image_files):
        img = Image.open(image_file)
        img.thumbnail(size=(item_size, item_size))

        background.paste(img, (x, 0))
        x = int(x + space + item_size)

    return background


# Entry point
print("Trail download helper\n")
topic = input("Enter a topic (e.g. Dinosaurs): ")
topic = topic.title()

# Create the output dir (if it doesn't already exist)
output_dir = os.path.join(OUTPUT_ROOT, topic)
os.makedirs(output_dir, exist_ok=True)

# Get a list of files already in the directory
files = glob.glob("?? *.jpg", root_dir = output_dir)
# We assume that they are numbered 01, 02, 03 and that there are no gaps.
# This will be true if created by this script, but may go awry if you fiddle with the contents.
num_results = len(files)
print(f"Starting from {num_results} items")

common_keywords = input("Enter any common keywords (e.g. line drawing): ")

while True:
    item_title = input("\nEnter item description (e.g. Stegosaurus) or enter to finish: ")
    if "" == item_title:
        break

    # Get the results
    tempdir = tempfile.TemporaryDirectory()
    storage = {'root_dir':tempdir.name}
    crawler = BingImageCrawler(storage=storage)
    crawler.set_logger(log_level=logging.WARNING)
    keyword = item_title + " " + common_keywords
    crawler.crawl(keyword=keyword, max_num=MAX_RESULTS)

    # Show the results
    candidates = glob.glob("*", root_dir=tempdir.name)
    candidates = [os.path.join(tempdir.name, candidate) for candidate in candidates]
    print(f"Candidates: {candidates}")
    combined = combine_images(candidates, item_size=THUMNAIL_SIZE, space=THUMNAIL_SIZE/5)
    combined.show()
    selection = input("Enter the image you want (e.g. 1 for first): ")
    selection_index = int(selection) - 1 # 0-base

    # Copy the result to the output dir
    index = "%02d" % (num_results+1)
    filename = f"{index} {item_title.title()}.jpg"
    src = candidates[selection_index]
    dest = os.path.join(output_dir, filename)
    shutil.move(src, dest)

    num_results += 1
    