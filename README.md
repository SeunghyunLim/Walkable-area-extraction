# Walkable-area-extraction
## Main functions
### 1. img2binList
```bash
def img2binList(img, lenWidth, GRID_SIZE=50, verbose=0):
  global DISTANCECOSTMAP
  return maze
```
- Convert RGB image to binary list. In this function, the image file is cropped first, and then converted to binary list. 
- Additionally, global variable __DISTANCECOSTMAP__ is created containing the information about the distance from every grid to nearing obstacles. This variable is calculated by _march_ function of fast marching method(fmm).
- The global variable __DISTANCECOSTMAP__ is for another pathplanning repository, *[Astar-with-Distance-cost](https://github.com/SeunghyunLim/Astar-with-Distance-cost), so this variable doesn't have a role in this repository.
- Parameters: __lenWidth__ is the actual width of the map in _cm_ scale, and __GRID_SIZE__ is the actual size of the grid in _cm_ scale.

| Original Image (SLAM) | Cropped Image | Binary List | DISTANCECOSTMAP |
|---|---|---|---|
|![a](https://github.com/SeunghyunLim/Walkable-area-extraction/blob/master/img/original_map_image.png)|![a](https://github.com/SeunghyunLim/Walkable-area-extraction/blob/master/img/cropped_map_image.png)|![a](https://github.com/SeunghyunLim/Walkable-area-extraction/blob/master/img/cropped_binary_list.png)|![a](https://github.com/SeunghyunLim/Walkable-area-extraction/blob/master/img/DISTANCECOSTMAP.png)|


### 2. walkable_area_contour
```bash
def walkable_area_contour(maze, x_real, y_real, verbose=0):
  return (contours[idxLargest], contourExceptions, idxLargest, idxException)
```
This function returns 
- __contours[idxLargest]__ : the largest contour containing the current position
- __contourExceptions__ : the exception contours
- __idxLargest__ and __idxException__ : their indexes

Find walkable and reachable area from the binary map, considering the current robot position, _x_real_ and _y_real_. 
After find every contour in the binary map, rearrange contours according to their contour area size. 
First, find the largest contour that includes the current robot position inside.
As we can see by intuition, the robot can move everywhere inside the largest contour, except for the contours inside the largest contour.
Therefore, the walkable area can be expressed as the inside area of _largest contour_ except for the _contourExceptions.
