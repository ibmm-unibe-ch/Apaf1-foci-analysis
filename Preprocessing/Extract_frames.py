#############################################
# Calvin Klein                              #
# August 2023                               #
#                                           #
# Python Script to extract individual       #
# frames from a tif movie to individual     #
# tif files                                 #
#############################################  


#################################
######## PART 0: Imports ########
#################################

import os
import sys
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np
import shutil


###################################
######## PART 2: Functions ########
###################################

def create_output_directory():
    """Create a new output directory."""
    path = os.getcwd()
    new_path = os.path.join(path, "extracted_frames")
    if not os.path.exists(new_path):
        os.makedirs(new_path)

def get_matching_files(full_list, substrings):
    """Retrieve matching files in the given movie directory."""
    files = os.listdir(full_list)
    return [s for s in files if all(sub in s for sub in substrings)]

def add_file_names(df, movies_directory, output_directory):
    """Add the corresponding filename to each line in the dataframe"""
    # Create 'file_name' column in dataframe;
    if 'file_name' not in df:
        df['file_name'] = ''
    df = df.mask(df == '')
    # Retrieve available file names that belong to each row in the list
    for index, row in df.iterrows():
        # Create Substrings
        acquisition_date = str(row['date'])
        position = f"p{str(row['imaging_position']).zfill(2)}"
        treatment = row['treatment']
        substrings_file = [acquisition_date, position, treatment]
        # Add the correct filename to the 'file_name' column
        file_value = get_matching_files(movies_directory, substrings_file)
        if file_value:
            file_string = str(file_value[0])
            df.at[index, 'file_name'] = file_string
    # Finalize Dataframe, clean it and return it    
    clean_death = df[df['file_name'].notna()].reset_index(drop=True).replace('NA', np.NaN)
    return clean_death

def extract_frames_of_dying_cells(df, movies_directory, output_directory):
    """Extract frames of dying cells without foci."""
    for index, row in df.iterrows():
        #Create naming scheme for image
        acquisition_date = str(row['date'])
        treatment = row['treatment']
        time_frames = str(row['frame_time'])
        position = 'p' + str(row['imaging_position']).zfill(2)
        cell_id = str(row['cell_id'])
        death_slice = str(row['frame_death'])[:-2]
        position_x = int(float(row['x']) * 1584/134.8)
        position_y = int(float(row['y']) * 1584/134.8)
        naming_scheme = acquisition_date + '_Apaf1_' + treatment + '_' + time_frames + 'min_' + position + '_Cell' + cell_id + '_DeathNoFoci_' + death_slice
        # Open and save correct slice of the stack file
        try:
            if pd.isna(df['frame_appearance_1'].iloc[index]):
                with Image.open(os.path.join(movies_directory, row['file_name'])) as img:
                    # Open Frames and save them as individual channel images
                    slices = [int(row['frame_death']*2-3), int(row['frame_death']*2-4)]
                    img.seek(slices[0])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch1.tiff"))
                    img.seek(slices[1])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch2.tiff"))                
                    # Create a mask for this slice
                    mask = Image.new('L', (1584, 1584))
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((position_x -30 , position_y -30, position_x +30, position_y +30), fill=(255), outline=(0))
                    mask.save(os.path.join(output_directory, f"{naming_scheme}_mask.tiff"), "TIFF")
                
        except (AttributeError, ValueError):
            continue

def extract_frames_of_dying_cells_2h_before(df, movies_directory, output_directory):
    """Extract frames of dying cells without foci."""
    for index, row in df.iterrows():
        #Create naming scheme for image
        acquisition_date = str(row['date'])
        treatment = row['treatment']
        time_frames = str(row['frame_time'])
        position = 'p' + str(row['imaging_position']).zfill(2)
        cell_id = str(row['cell_id'])
        death_slice = str(row['frame_death'])[:-2]
        position_x = int(float(row['x']) * 1584/134.8)
        position_y = int(float(row['y']) * 1584/134.8)
        naming_scheme = acquisition_date + '_Apaf1_' + treatment + '_' + time_frames + 'min_' + position + '_Cell' + cell_id + '_DeathNoFoci_' + death_slice + '_2h'
        # Open and save correct slice of the stack file
        try:
            if pd.isna(df['frame_appearance_1'].iloc[index]):
                with Image.open(os.path.join(movies_directory, row['file_name'])) as img:
                    slices = [int(row['frame_death']*2-49), int(row['frame_death']*2-50)]
                    if slices[0] < 0: 
                        slices = [0,1]
                    img.seek(slices[0])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch1.tiff"))
                    img.seek(slices[1])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch2.tiff"))
                    # Create a mask for this slice
                    mask = Image.new('L', (1584, 1584))
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((position_x -30 , position_y -30, position_x +30, position_y +30), fill=(255), outline=(0))
                    mask.save(os.path.join(output_directory, f"{naming_scheme}_mask.tiff"), "TIFF")
        except (AttributeError, ValueError):
            continue

def extract_frames_of_cells_with_foci(df, movies_directory, output_directory):
    """Extract frames of cells with foci."""
    for index, row in df.iterrows():
        acquisition_date = str(row['date'])
        treatment = row['treatment']
        time_frames = str(row['frame_time'])
        position = f"p{str(row['imaging_position']).zfill(2)}"
        cell_id = str(row['cell_id'])
        foci_slice = str(row['frame_appearance_1'])[:-2]
        position_x = int(float(row['x']) * 1584/134.8)
        position_y = int(float(row['y']) * 1584/134.8)
        naming_scheme = f"{acquisition_date}_Apaf1_{treatment}_{time_frames}min_{position}_Cell{cell_id}_Foci_{foci_slice}"
        try:
            if not pd.isna(df['frame_appearance_1'].iloc[index]):
                with Image.open(os.path.join(movies_directory, row['file_name'])) as img:
                    slices = [int(row['frame_appearance_1']*2-3), int(row['frame_appearance_1']*2-4)]
                    img.seek(slices[0])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch1.tiff"))
                    img.seek(slices[1])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch2.tiff"))
                    # Create a mask for this slice
                    mask = Image.new('L', (1584, 1584))
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((position_x -30 , position_y -30, position_x +30, position_y +30), fill=(255), outline=(0))
                    mask.save(os.path.join(output_directory, f"{naming_scheme}_mask.tiff"), "TIFF")
        except (AttributeError, ValueError):
            continue

def extract_frames_of_cells_with_foci_2h_before(df, movies_directory, output_directory):
    """Extract frames of cells with foci."""
    for index, row in df.iterrows():
        acquisition_date = str(row['date'])
        treatment = row['treatment']
        time_frames = str(row['frame_time'])
        position = f"p{str(row['imaging_position']).zfill(2)}"
        cell_id = str(row['cell_id'])
        foci_slice = str(row['frame_appearance_1'])[:-2]
        position_x = int(float(row['x']) * 1584/134.8)
        position_y = int(float(row['y']) * 1584/134.8)
        naming_scheme = f"{acquisition_date}_Apaf1_{treatment}_{time_frames}min_{position}_Cell{cell_id}_Foci_{foci_slice}_2h"
        try:
            if not pd.isna(df['frame_appearance_1'].iloc[index]):
                with Image.open(os.path.join(movies_directory, row['file_name'])) as img:
                    slices = [int(row['frame_appearance_1']*2-49), int(row['frame_appearance_1']*2-50)]
                    if slices[0] < 0: 
                        slices = [0,1]
                    img.seek(slices[0])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch1.tiff"))
                    img.seek(slices[1])
                    img.save(os.path.join(output_directory, f"{naming_scheme}_Ch2.tiff"))
                    # Create a mask for this slice
                    mask = Image.new('L', (1584, 1584))
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((position_x -30 , position_y -30, position_x +30, position_y +30), fill=(255), outline=(0))
                    mask.save(os.path.join(output_directory, f"{naming_scheme}_mask.tiff"), "TIFF")
        except (AttributeError, ValueError):
            continue

def cleanup_files(output_directory):
    """Cleanup the extracted files."""
    extracted_files = os.listdir(output_directory)
    folder_path = output_directory
    for file in extracted_files:
        date = file.split("_")[0]
        # Create a new subfolder with the extracted date as the folder name
        subfolder_path = os.path.join(folder_path, date)
        os.makedirs(subfolder_path, exist_ok=True)
        # Move the file to the corresponding subfolder
        file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(subfolder_path, file)
        shutil.move(file_path, new_file_path)


######################################
######## PART 3: Main Program ########
######################################


def main():

    # Check if correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 extract_frames.py <path/to/input_csv>")
        return
    
    # Check if the help argument is provided
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Usage: python3 extract_frames.py <input_csv>")
        print("This script extracts frames of movies")
        print("according to the frame_appearance_1 and ")
        print("the frame_death column in the input csv")
        return
    
    # Variables
    csv_sheet = sys.argv[1]
    movies_directory = "./movies"
    output_directory = "./extracted_frames"
    df = pd.read_csv(csv_sheet)

    # Creating Directories 
    print('Creating Output Directories...')
    create_output_directory()

    # Dataframe Manipulation
    print('Adding file_names column to Dataframe...')
    df = add_file_names(df, movies_directory, output_directory)

    # Extraction 1
    print('Extracting frames of dying cells without foci...')
    extract_frames_of_dying_cells(df, movies_directory, output_directory)
    extract_frames_of_dying_cells_2h_before(df, movies_directory, output_directory)

    # Extraction 2
    print('Extracting frames of cells with foci...')
    extract_frames_of_cells_with_foci(df, movies_directory, output_directory)
    extract_frames_of_cells_with_foci_2h_before(df, movies_directory, output_directory)

    # Cleanup
    print('Cleaning Data...')
    cleanup_files(output_directory)
    print('Done!')

if __name__ == "__main__":
    main()

