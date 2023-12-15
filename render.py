#!/usr/bin/env python3

"""
Create a trail (as HTML/CSS) from a downloaded directory.
A trail consists of several picture sheets and one table to fill in.
"""

import glob
import os
import re
import shutil

OUTPUT_ROOT = "trails"

# The various HTML templates from which to create the document.
# (We could alternatively use an intelligent template like Jinja, but it seems overkill here.) 
HTML_HEADER = '<!DOCTYPE html><html><head><title>__HEADING__</title><link rel="stylesheet" href="trail.css"/><meta charset="UTF-8"/></head><body>'
HTML_PICTURE_PAGE = '<div class="page"><div class="picturepage"><div class="number">__NUMBER__</div><div class="picture"><img src="__IMAGE_FILE__"/></div><div class="name">__NAME__</div></div></div>'
HTML_TABLE_PAGE = '<div class="page"><div class="formpage"><div class="title">__TRAIL_TITLE__</div><div class="fillinform">__TABLE__</div></div></div>'
HTML_TABLE_HEADER = '<table>'
HTML_TABLE_ROW = '<tr><td class="answernumber">__NUMBER__</td><td class="answer"/></tr>'
HTML_TABLE_FOOTER = '</table>'
HTML_FOOTER = '</body></html>'

# Entry point
print("Trail renderer\n")

# Get all the downloaded trails
trail_dirs = glob.glob("*", root_dir=OUTPUT_ROOT)
num_trails = len(trail_dirs)
for i in range(0, num_trails):
    print(f"({i+1}) {trail_dirs[i]}")
if num_trails == 0:
    print("Create a trail first with download.py")
    exit(0)
if num_trails == 1:
    trail_index = 0
else:
    trail_index = int(input("Choose a trail: "))-1
trail_name = trail_dirs[trail_index]
trail_dir = os.path.join(OUTPUT_ROOT, trail_name)

print(f"Creating {trail_name} trail")

# Get all files in the dir
files = glob.glob("?? *.jpg", root_dir=trail_dir)
files.sort()

# Create an array of (index, name, filename)
items = []
for file in files:
    # Get name and number
    # 01 Stegosaurus.jpg
    match = re.match("(\d{2}) (.+)\.jpg", file)
    index = str(int(match.group(1))) # Remove leading 0s
    name = match.group(2)
    item = (index, name, file)
    items.append(item)
    

# Create the html
trail_file = os.path.join(trail_dir, "trail.html")
with open(trail_file, "w") as html:
    header = HTML_HEADER.replace("__HEADING__", trail_name + " trail")
    html.write(header)

    table = HTML_TABLE_HEADER

    for item in items:
        index = item[0]
        name = item[1]
        file = item[2]
        page = HTML_PICTURE_PAGE.replace("__NUMBER__", index).replace("__NAME__", name).replace("__IMAGE_FILE__", file)
        html.write(page)

        table_row = HTML_TABLE_ROW.replace("__NUMBER__", index)
        table += table_row

    table += HTML_TABLE_FOOTER
    table_page = HTML_TABLE_PAGE.replace("__TRAIL_TITLE__", trail_name).replace("__TABLE__", table)
    html.write(table_page)

    html.write(HTML_FOOTER)

# Drop in the CSS
shutil.copyfile("trail.css", os.path.join(trail_dir, "trail.css"))

print("Done")