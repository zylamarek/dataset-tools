# Dataset tools

Command line tool for batch image data processing.  

Apply operations (filters and functions) to images. Operations can be stacked and applied with different parameters in one call. Easy to implement new filters and functions.  

Images may be treated as a sequence. In such case extracted meta data can be smoothed and missing values may be filled in (functions only).

Filters:
- Duplicate - removes duplicates
- FaceDetection - finds images containing at least one face
- MinDimension - removes images smaller than given threshold
- MouthClosed - finds images where the first detected face has mouth closed

Functions:
- AlignFace - crops, rotates and scales face; uses Kalman smoother for sequential input
- CropFace - crops an image to contain the face only
- NormalizeSegmentation - scales pixel values from (0, N-1) to (0, 255)
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
