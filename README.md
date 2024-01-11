
# Image alignment for image preprocessing

Image preprocessing script wchich can be used to align the image subject as follows.
   
   Non-Aligned Image <img src="assets/non_aligned.JPG" alt="Non-Aligned Image" width="200" height="200" /> Aligned Image  <img src="assets/aligned.JPG" alt="Aligned Image" width="200" height="200" />


# Table of Contents
 [Requirements](#requirement) | [Detailed Documentation](#detailed-documentation) | [Some constrains](#some-constrains)

# Requirement

- Ubuntu 20.04 & 22.04 or Windows 10 & Windows 11
- Python 3.8.*
- numpy 1.24.4
- opencv-python 4.8.1


  
******************

# Detailed Documentation

### Data Preparation

Prepare a data set with the following structure

```
C:
│ 
└── image_alignment
    ├── data
    │   └──001
    │       ├── good
    │       │    └── [SOME GOOD IMAGE]
    │       ├── bad
    │            └── [SOME BAD IMAGE]
    └── main.py
```

### Startup
Run this code to process the dataset
```sh
python main.py --padding=50 --input=data\\001 --output=results --min_threshold=100 --max_threshold=250 --height_factor=5.03
```

#### parameter reference
```sh    
    input:      →     dataset path
    output:      →      Result path
    min_threshold:      →    minimum threshold for gray scale conversion   
    max_threshold:      →    maximum threshold for gray scale conversion
    padding:            →    after align the subject image will be cropped, padding is to add the pixel around the subject
    height_factor:      →    after adding the pixel, if the subject is rectangular then this factor will be adjusted for making the image square
```

#### Output after processing
```
C:
│ 
└── image_alignment
    ├── data
    │   └──001
    │       ├── good
    │       │    └── [SOME GOOD IMAGE]
    │       ├── bad
    │            └── [SOME BAD IMAGE]
    ├── results
    │   └──001
    │       ├── good
    │       │    └── [SOME GOOD IMAGE]
    │       ├── bad
    │            └── [SOME BAD IMAGE]
    └── main.py

```
# Some constrains 

Example:
- it works only when the objects are rectangular with a clear and uniform background.
- It may raise error to read dataset name written on Japanese, that time it may be required to rename in English
- This script is tested on [001_基板対電線接続用コネクタ](https://chowagiken.sharepoint.com/:f:/g/CorporatePlanning/licence-business/EjFwj7ulvPZCm9kxFcquJ9cB-LmoEBTMTrcdealR7HTSQA?e=EVpr0p) and [002_サミコン1600シリーズコネクタユニット](https://chowagiken.sharepoint.com/:f:/g/CorporatePlanning/licence-business/ElFF6Gvdme9Gp4xWfL_uLiUBPL3FsysrKoKo2WgUtp3caA?e=tskCQf) these datasets
- IMGP0610.JPG, and IMGP0621.JPG images were not processed properly from 001_基板対電線接続用コネクタ dataset
- IMGP0570.JPG, this image was not processed properly from 002_サミコン1600シリーズコネクタユニット dataset