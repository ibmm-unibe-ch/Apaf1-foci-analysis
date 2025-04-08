
This Python script was developed to automate the extraction of specific image frames from multi-frame .tif (TIFF) movies based on cell imaging metadata. It supports the extraction of frames where cell events occur such as appearance of foci or cell death along with time-matched control frames (e.g., 2 hours before the event). The script also generates corresponding elliptical masks centered on cell coordinates for downstream analysis.

## Key Features
Parses a user-provided CSV file containing experimental metadata (e.g., frame indices, positions, treatments).

Locates matching TIFF movie files in a specified directory.

Extracts and saves relevant frames as individual TIFF images.

Generates circular masks centered on specified (x, y) coordinates from the CSV file.

Organizes extracted files into date-based subfolders for easy access.

Includes support for both:

Cells with foci appearance

Dying cells without foci

Control frames (~2 hours before events)


## Directory Structure

Input:

./metadata.csv

./movies/ #directory containing TIFF stacks

Output:

./extracted_frames/ with sorted subfolders by acquisition date


## Requirements and Installation

The analysis was performed mainly with the open-source software [CellProfiler](https://cellprofiler.org/).
Install it according to the guidelines on their website.

The data preprocessing script only has minimal dependencies. Depending on what kind of virtual environment you like, there are files to create 
a conda or pip environment.
  
  - environment.yml &rightarrow; conda
  - requirements.txt &rightarrow; pip

Either use:

```bash
conda env create --name tif-extractor-env --file=environments.yml
```

or:

```bash
pip install -r requirements.txt
```



## Usage

To run the script:

```bash
python3 extract_frames.py path/to/input.csv
```

The script needs to be run from the folder containing the ./movies folder.




