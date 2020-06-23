# Walkable-area-extraction
## Main functions
### 1. img2binList
```bash
def img2binList(img, lenWidth, GRID_SIZE=50, verbose=0):
  global DISTANCECOSTMAP
  return maze
```
Convert RGB image to binary list. In this function, the image file is cropped first, and then converted to binary list. Additionally, global variable __DISTANCECOSTMAP__ is created containing the information about the distance from every grid to nearing obstacles. This variable is calculated by _march_ function of fast marching method(fmm).  
Parameters: __lenWidth__ is the actual width of the map in _cm_ scale, and __GRID_SIZE__ is the actual size of the grid in _cm_ scale.

| Original Image (SLAM) | Cropped Image | Binary List | DISTANCECOSTMAP |
|---|---|---|---|
|![a](https://github.com/SeunghyunLim/Walkble-area-extraction/blob/master/img/original_map_image.png)|![a](https://github.com/SeunghyunLim/Walkble-area-extraction/blob/master/img/cropped_map_image.png)|![a](https://github.com/SeunghyunLim/Walkble-area-extraction/blob/master/img/cropped_binary_list.png)|![a](https://github.com/SeunghyunLim/Walkble-area-extraction/blob/master/img/DISTANCECOSTMAP.png)|
