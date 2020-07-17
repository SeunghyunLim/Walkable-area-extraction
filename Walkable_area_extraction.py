import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import time
import random



def convert2list(img):
    height, width = img.shape
    maze = np.zeros((height, width), np.uint8)
    for i in range(width):
        for j in range(height):
            maze[j][i] = 1 if img[j][i] > 0 else 0
    return maze.tolist()

def img2binList(img, lenWidth, GRID_SIZE=50, verbose=0):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, unreversed_gray = cv2.threshold(gray, 112, 255, cv2.THRESH_BINARY)
    _, gray = cv2.threshold(gray, 112, 255, cv2.THRESH_BINARY_INV)
    if verbose:
        cv2.imshow("Reversed binary", gray)
        cv2.waitKey(0)

    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    locs = []

    height, width = gray.shape
    tmp = np.zeros((height, width), np.uint8)

    idxLargest = 0
    areaLargest = 0
    # loop over the contours
    for (i, c) in enumerate(cnts):
        # compute the bounding box of the contour, then use the
        # bounding box coordinates to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        if w * h > areaLargest:
            idxLargest = i
            areaLargest = w * h
        cv2.rectangle(tmp, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if verbose:
        # print("found largest contour outline")
        cv2.imshow("Contour lectangulars", tmp)
        cv2.waitKey(0)

    # print("cropping image as largest contour")
    (x, y, w, h) = cv2.boundingRect(cnts[idxLargest])
    gray = gray[y:y + h, x:x + w]
    unreversed_gray = unreversed_gray[y:y + h, x:x + w]
    if verbose:
        cv2.imshow("Cropped image", cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(0)
    global mapWidth
    global mapHeight
    mapWidth = (int)(lenWidth // GRID_SIZE)
    mapHeight = (int)((h / w) * lenWidth // GRID_SIZE)
    print("the map will be created by the size: " + str(mapWidth) + " X " + str(mapHeight))
    resized_gray = imutils.resize(gray, width=mapWidth)  # resize the map for convolution
    _, resized_gray = cv2.threshold(resized_gray, 1, 255, cv2.THRESH_BINARY)

    maze = convert2list(resized_gray)
    my_maze = np.array(maze)


    # cv2.destroyAllWindows()
    return maze

def walkable_area_contour(maze, x_real, y_real, verbose=0):
    maze = np.array(maze).astype(np.uint8)
    maze *= 255
    maze = cv2.resize(maze, None, fx=7, fy=7, interpolation=cv2.INTER_NEAREST)
    _, contoured_maze = cv2.threshold(maze, 112, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(contoured_maze, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    idxLargest = 0
    idxException = []
    areaLargest = 0
    contour_list = []
    smaller_contour_index = []
    ordered_contour_list = []
    contourExceptions = []

    for (i, c) in enumerate(contours):
        # compute the bounding box of the contour, then save their index with
        # the size of the bounding box
        (x, y, w, h) = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        contour_list.append([i, area])
    print("contour list :", contour_list)
    # sort the contour list according to their size of the bounding box
    ordered_contour_list = sorted(contour_list, key = lambda x : x[1]) #smallest to largest
    rev_ordered_contour_list = list(reversed(ordered_contour_list))  #ordered_contour_list.reverse() #largest to smallest
    print("larest to smallest : ", rev_ordered_contour_list)
    for (i, c) in enumerate(contours):
        if cv2.pointPolygonTest(contours[rev_ordered_contour_list[i][0]], (x_real * 7, y_real * 7), False) == 1:
            idxLargest = rev_ordered_contour_list[i][0]
            num_of_smaller = len(contour_list)-(i+1)
            for j in range(num_of_smaller):
                smaller_contour_index.append(ordered_contour_list[j][0])
            reference_idx = i-1
            #print(idxLargest, reference_idx)
            break
    # idxLargest means the index of the largest contour that includes current position
    # smaller_contour_list means the list of indext that has smaller bonding boxes than idxLargest

    # check the contours in smaller_contour_index whether they are included in idxLargest or not
    for i in smaller_contour_index:
        if hierarchy[0][i][3] == -1:
            # when the contour with i index are not included in any other contour
            continue
        elif hierarchy[0][i][3] == idxLargest:
            # when the contour with i index are direct child of the idxLargest contour
            idxException.append(i)
            continue
        else :
            j = hierarchy[0][i][3]
            while j != -1:
                if j == idxLargest:
                    idxException.append(i)
                    break
                else:
                    j = hierarchy[0][j][3]

    for i in idxException:
        contourExceptions.append(contours[i])

    if verbose:
        cv2.drawContours(contoured_maze, [contours[idxLargest]], 0, (112, 0, 0), 3)
        for i in idxException:
            cv2.drawContours(contoured_maze, [contours[i]], 0, (112, 0, 0), 3)
        cv2.imshow("contoured", contoured_maze)
        cv2.waitKey(0)

    return (contours[idxLargest], contourExceptions, idxLargest, idxException)


def random_reachable_goal(area, x_range, y_range, verbose=0):
    starting_time = time.time()
    contour = area[0]
    contourExceptions = area[1]
    idxLargest = area[2]
    while True:
        count = 0
        x = random.randrange(x_range)
        y = random.randrange(y_range)
        #print(cv2.pointPolygonTest(contour, (x * 7, y * 7), False))]
        if idxLargest == 0:
            if cv2.pointPolygonTest(contour, (x * 7, y * 7), False) == 1:
                return (y, x)
                break
        if cv2.pointPolygonTest(contour, (x * 7, y * 7), False) == 1:
            for c in contourExceptions:
                if cv2.pointPolygonTest(c, (x * 7, y * 7), False) == -1:
                    count += 1
            if count == len(contourExceptions):
                return (y, x)
                break
        #    if cv2.pointPolygonTest(reference_contour, (x * 7, y * 7), False) == -1:
        #        return (y, x)
        #        break
    if verbose:
        print("Curiosity Engine Calculation Time :", time.time() - starttime)

if __name__ == '__main__':
    #img = cv2.imread("E5_223.jpg")
    img = cv2.imread("lobby3.jpg")
    cv2.imshow('Original map image', img)
    cv2.waitKey(0)
    starttime = time.time()
    maze = img2binList(img, lenWidth=500.0, GRID_SIZE=5, verbose=1)  # all unit is cm
    x_real_initial = 20
    y_real_initial = 20
    area = walkable_area_contour(maze, x_real_initial, y_real_initial, verbose=0)
    print("time :", time.time() - starttime)
    while True:
        try:
            # start = (7, 7)
            # start = (10, 25)
            start = (x_real_initial, y_real_initial)
            end = random_reachable_goal(area, mapWidth, mapHeight)
            print("Start = ", start, "and End = ", end)
            showmaze = np.array(maze).astype(np.uint8)
            showmaze *= 255
            showmaze[start[0]][start[1]] = 150
            showmaze[end[0]][end[1]] = 150
            showmaze = cv2.resize(showmaze, None, fx=7, fy=7, interpolation=cv2.INTER_NEAREST)
            cv2.imshow('Walkable Area Extraction', showmaze)
            cv2.waitKey(0)
        except KeyboardInterrupt:
            print("interrupted")
            cv2.destroyallwindows()
            break
