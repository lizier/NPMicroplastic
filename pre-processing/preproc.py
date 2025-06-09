#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import markers
from pathlib import Path

def preproc( image ):
    try:
        imgb = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255,255,255))
        corners, ids, imgb = markers.detectMarkers( imgb )   
        img_preproc = markers.correctDeformation(imgb, corners)
    except:
        img_preproc = ''
    return img_preproc


if __name__ == '__main__':
    
    inputpath = '../data/'
    outputpath = './data/'
    
    images = []

    for currentpath, folders, files in os.walk(inputpath):
        rel = os.path.relpath(currentpath,inputpath)
        dest = os.path.join(outputpath,rel)
        if not os.path.exists(dest):
            os.makedirs(dest)
        for file in files:        
            fi = os.path.join(currentpath, file)
            fo = os.path.join(dest, Path(file).with_suffix('.png'))
            if os.path.isfile(fi):
                if fi.endswith('.jpg'):
                    images.append([ fi, fo ])
     
    for f in images:    
         if not os.path.isfile(f[1]):
            img = cv2.imread(f[0])
            print(f[1])
            img_preproc = preproc( img )
            cv2.imwrite(f[1], img_preproc)
    
    
