#!/usr/bin/env python3



import numpy as np
import cv2 as cv
import os


def calculate_iou(box1, box2):
    # box1 and box2 are lists or tuples of [x, y, w, h] values
    
    # Get the coordinates of the top-left and bottom-right corners of each bounding box
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    x1_tl, y1_tl, x1_br, y1_br = x1, y1, x1 + w1, y1 + h1
    x2_tl, y2_tl, x2_br, y2_br = x2, y2, x2 + w2, y2 + h2
    
    # Calculate the coordinates of the intersection bounding box
    x_int_tl, y_int_tl = max(x1_tl, x2_tl), max(y1_tl, y2_tl)
    x_int_br, y_int_br = min(x1_br, x2_br), min(y1_br, y2_br)
    
    # Calculate the area of intersection
    if x_int_tl > x_int_br or y_int_tl > y_int_br:
        return 0.0 # no intersection
    else:
        int_area = (x_int_br - x_int_tl) * (y_int_br - y_int_tl)
    
    # Calculate the area of union
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - int_area
    
    # Calculate the IOU score
    iou_score = int_area / union_area
    
    return iou_score
