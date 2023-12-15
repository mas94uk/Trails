# Trails
Create printable treasure hunt-style trails for kids.

You choose a topic (e.g. "Dinosaurs") and several items in that category (e.g. "Stegosaurus", "Triceratops").
The script downloads a selection of images for each item from Bing. You choose one.
The result is rendered to HTML for you to print.

# To use
* Clone the repository.
* `python3 -m venv .venv` to create a virual environment
* `source .venv/bin/activate` to activate the virtual environment
* `python3 -m pip install -r requirements.txt` to install the dependencies
* Run `./download.sh` and follow the prompts to select and download images
* Run `./render.sh` to build the trail as HTML
* Open the HTML in your browser and print it.

Trails are rendered for A4 paper. Use your printer's 2-up or 4-up printing option to print them smaller.
