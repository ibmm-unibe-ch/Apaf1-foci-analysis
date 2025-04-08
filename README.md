
This Python script was developed to automate the extraction of specific image frames from multi-frame .tif (TIFF) movies based on manually curated cell imaging metadata. It supports the extraction of frames where cell events occur such as appearance of foci or cell death along with time-matched control frames (e.g., 2 hours before the event). The script also generates corresponding elliptical masks centered on cell coordinates for downstream analysis.

## Key Features

- Parses a user-provided **CSV file** containing experimental metadata (e.g., frame indices, positions, treatments).
- Locates matching multi-frame **TIFF movie files** in a specified directory.
- Extracts and saves specific frame slices as individual TIFF images (per channel).
- Generates **circular masks** centered on (x, y) coordinates from the metadata.
- Organizes output files into **date-based subfolders** for easier navigation.



## Directory Structure

Input:

```
./Extract_frames.py 

./metadata.csv

./movies/ #directory containing TIFF stacks
```


Output:

```
./extracted_frames/ # with sorted subfolders by acquisition date
```

## Requirements and Installation

This script has minimal dependencies. You can set up the environment using either **conda** or **pip**, depending on your preference.

### Option 1: Using Conda
```bash
conda env create --name tif-extractor-env --file=environment.yml
conda activate tif-extractor-env
```

### Option 2: Using pip

```bash
pip install -r requirements.txt
```


The primary analysis of Apaf1 foci was performed with [CellProfiler](https://cellprofiler.org/), which is not included in the environment. Please install it separately using their official installation instructions. The cellprofiler-pipeline file for reproducing our pipeline can be found in the **CellProfiler_Pipeline** folder. 



## Usage

To run the preprocessing script:

```bash
python3 extract_frames.py path/to/input.csv
```

Important: The script must be run from the directory that contains the ./movies folder.




