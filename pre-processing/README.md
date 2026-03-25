# Pre-Processing Step
| Input | Output |
| ----- | ------ |
| <img src="https://github.com/lizier/NPMicroplastic/blob/main/data/Sample/31.01/DSC_0925.jpg" width="150" height="auto"/> | <img src="https://github.com/lizier/NPMicroplastic/blob/main/pre-processing/data/Sample/31.01/DSC_0925.png" width="150" height="auto"/> |


# Objectives:

The image preprocessing stage consists of:
* ArUco Marker detection: recognition, identification, and ordering
* Orientation correction
* Image resizing: standardization of all images to the same size
* Distortion correction: inverse perspective transformation to correct camera distortions

# Description 

Define the input and output paths in the code using the variables `inputpath` and `outputpath`. Organize the dataset into a hierarchical directory structure, where each individual has a dedicated folder containing all their images. Within each individual’s folder, create subfolders for each capture day.

Ensure that the ordering of images (e.g., corresponding to fingers) remains consistent across all days and individuals.

The program will traverse all images in the `inputpath` directory and reproduce the same directory structure in `outputpath`, saving the corresponding preprocessed images in their respective locations.

# Execution

##
    python prepoc.py
