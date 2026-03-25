# Post-Processing

| Output Data | Output Image |
| ----------- | ------------ |
| [CSV Data](data/data.csv | width=100) | ![Post-Processing](data/Sample/31.01/DSC_0925.png | width=100) |

# Description

The code generates a composite image divided into four quadrants:

* the original image
* the binarized image of the nail polish
* the original image with the nail polish segmentation overlaid
* a final quadrant showing only the isolated nail polish

In addition, the program creates a CSV file named `data.csv`, containing all extracted data for every nail polish sample across all individuals.

Define the paths in the code using the variables inputpath, binatypath, and outputpath. The inputpath should point to the directory generated during the preprocessing stage, while the binatypath corresponds to the directory produced by the segmentation stage. The outputpath will be used to store the results.

## Command

##
    python proc.py
