#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

def getCenterRadius( corners ):
    centrox = centroy = 0.0;
   
    if len(corners) == 4:
        for p in corners:
            for i in range(4):
                centrox += p[0][i][0]
                centroy += p[0][i][1]
        radius = max( abs(corners[0][0][0][0] - corners[0][0][1][0]), abs(corners[0][0][0][0] - corners[0][0][2][0]))
    else:
        radius = 0
        
    return [int(centrox/16), int(centroy/16)], int(radius/6)

def detectMarkers( image ):
    
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    aruco_parameters =  cv2.aruco.DetectorParameters_create()
    aruco_parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX;
    aruco_parameters.adaptiveThreshWinSizeMax = 100
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_parameters)
    
    assert len(ids) == 4
    
    mx = image.shape[0]/2
    dx = image.shape[0]/5
    my = image.shape[1]/2
    dy = image.shape[1]/5
    
    idx = np.zeros(4, dtype=int)
    idx -= 1
    
    for i in range(4):
        for b in range(4):
            if ids[b][0] == i+1:
                idx[i] = b;

    assert np.all(idx >= 0)
    
    if corners[idx[0]][0][0][0] < mx + dx and corners[idx[0]][0][0][1] < my + dy and \
        corners[idx[2]][0][0][0] < mx + dx and corners[idx[2]][0][0][1] > my - dy and \
        corners[idx[3]][0][0][0] > mx - dx and corners[idx[3]][0][0][1] > my - dy and \
        corners[idx[1]][0][0][0] > mx - dx and corners[idx[1]][0][0][1] < my + dy :
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_parameters)
    elif corners[idx[1]][0][0][0] < mx + dx and corners[idx[1]][0][0][1] < my + dy and \
        corners[idx[0]][0][0][0] < mx + dx and corners[idx[0]][0][0][1] > my - dy and \
        corners[idx[2]][0][0][0] > mx - dx and corners[idx[2]][0][0][1] > my - dy and \
        corners[idx[3]][0][0][0] > mx - dx and corners[idx[3]][0][0][1] < my + dy :
            image = cv2.rotate(image, cv2.ROTATE_180)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_parameters)
    elif corners[idx[3]][0][0][0] < mx + dx and corners[idx[3]][0][0][1] < my + dy and \
        corners[idx[1]][0][0][0] < mx + dx and corners[idx[1]][0][0][1] > my - dy and \
        corners[idx[0]][0][0][0] > mx - dx and corners[idx[0]][0][0][1] > my - dy and \
        corners[idx[2]][0][0][0] > mx - dx and corners[idx[2]][0][0][1] < my + dy :
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_parameters)
    else:
        assert  corners[idx[2]][0][0][0] < mx + dx and corners[idx[2]][0][0][1] < my + dy and \
            corners[idx[3]][0][0][0] < mx + dx and corners[idx[3]][0][0][1] > my - dy and \
            corners[idx[1]][0][0][0] > mx - dx and corners[idx[1]][0][0][1] > my - dy and \
            corners[idx[0]][0][0][0] > mx - dx and corners[idx[0]][0][0][1] < my + dy 
                
    return corners, ids, image


def correctOrientation( image ):
   
    return

def correctScale( image, corners ):
    
    return

def getOrder( corners ):
    centro = getCenter(corners)
    
    diff = np.array(corners) - np.array(centro)
    diffp = np.less(diff,[ 0, 0]).tolist()
    
    top_left = diffp.index( [ True, True ] );
    top_right = diffp.index( [ False, True ] );
    bottom_right = diffp.index( [ False, False ] );
    bottom_left = diffp.index( [ True, False ] );
               
    return top_left, top_right, bottom_right, bottom_left
    
def getCenter( corners ):
    centrox = centroy = 0.0;
    for i in range(4):
        centrox += corners[i][0]
        centroy += corners[i][1]
   
    return [ centrox/4, centroy/4 ]
    

def getBoundaries( corners ):
    if len(corners) == 4:
        orders = []
        centers = []
        for p in corners:
            orders.append( getOrder(p[0]) )
            centers.append( getCenter(p[0]) )
       
        porder = getOrder(centers)
         
        top_left = corners[porder[0]][0][orders[porder[0]][0]]
        top_right = corners[porder[1]][0][orders[porder[1]][1]]
        bottom_right = corners[porder[2]][0][orders[porder[2]][2]]
        bottom_left = corners[porder[3]][0][orders[porder[3]][3]]

        return [top_left, top_right, bottom_left, bottom_right]
    

def correctDeformation( image, corners ): 
    
    # https://github.com/codegiovanni/Warp_perspective/blob/main/warp_perspective.py
    input_points = np.float32( getBoundaries(corners) )
    max_width = 800 #4000
    max_height = 1000 #5000

    converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
    
    matrix = cv2.getPerspectiveTransform(input_points, converted_points, cv2.DECOMP_SVD)
    img_output = cv2.warpPerspective(image, matrix, (max_width, max_height), cv2.WARP_INVERSE_MAP)
        
    return img_output


def detect( image ):
    
    corners, ids, image = detectMarkers( image )   
   
    return getCenterRadius( corners ), image
