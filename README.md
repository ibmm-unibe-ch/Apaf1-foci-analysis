
This Python script was developed to automate the extraction of specific image frames from multi-frame .tif (TIFF) movies based on cell imaging metadata. It supports the extraction of frames where cell events occur?such as appearance of foci or cell death?along with time-matched control frames (e.g., 2 hours before the event). The script also generates corresponding elliptical masks centered on cell coordinates for downstream analysis.

## Key Features
Parses a user-provided CSV file containing experimental metadata (e.g., frame indices, positions, treatments).

Locates matching TIFF movie files in a specified directory.

Extracts and saves relevant frames as individual TIFF images.

Generates circular masks centered on specified (x, y) coordinates.

Organizes extracted files into date-based subfolders for easy access.

Includes support for both:

Cells with foci appearance

Dying cells without foci

Control frames (~2 hours before events)

## Directory Structure
Input:

CSV metadata file

./movies/ directory containing TIFF stacks

Output:

./extracted_frames/ with sorted subfolders by acquisition date

## Usage

```bash
Copy
Edit
python3 extract_frames.py path/to/input.csv
```


## Installation

- Requirements files &rightarrow; depending what kind of virtual environment you like, there already is a (basically) empty file
  - environment.yml &rightarrow; conda
  - requirements.txt &rightarrow; pip

