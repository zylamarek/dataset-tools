# Dataset tools

Command line tool for batch image data processing.  

Apply operations (filters and functions) to images. Operations can be stacked and applied with different parameters in one call. Easy to implement new filters and functions.

Filters:
- Duplicate - removes duplicates
- FaceDetection - finds images containing at least one face
- MinDimension - removes images smaller than given threshold

Functions:
- CropFace - crops an image to contain the face only
- Resize - resizes an image keeping the aspect ratio

## Install

```
bash install.sh
```

## Usage

```
. env.sh
python main.py data/example1 Duplicate CropFace Resize(256)
```
