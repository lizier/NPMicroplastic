#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cv2
import os
import csv
import numpy as np
from pathlib import Path


def r_unha( fundo, unha ):    
    #f = np.where( unha[:,:] == [130,255,79] )
    #u = np.where( unha[:,:] == [0,0,255] )
    u = np.where( unha[:,:] == 0 )
    r = np.copy(fundo)
    r[ u[0], u[1],0 ] = 0
    r[ u[0], u[1],1 ] = 0
    r[ u[0], u[1],2 ] = 0
    return r

def r_fundo( fundo, unha ):    
    #f = np.where( unha[:,:] == [130,255,79] )
    f = np.where( unha[:,:] == 255 )
    r = np.copy(fundo)
    r[ f[0], f[1],0 ] = 0
    r[ f[0], f[1],1 ] = 0
    r[ f[0], f[1],2 ] = 0
    return r

    

def proc( image ):
    
    img_pre = cv2.imread( image[0] )

    img_gray = cv2.imread( image[1], cv2.IMREAD_GRAYSCALE )    
    
    im_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)[1]

    kernel = np.ones((5,5),np.uint8)

    opening = cv2.morphologyEx(im_bin, cv2.MORPH_OPEN, kernel)
    openingclosing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    #closing = cv2.morphologyEx(im_bw, cv2.MORPH_CLOSE, kernel)
    #closingopening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)  
    
    img_oc = cv2.cvtColor(openingclosing, cv2.COLOR_GRAY2BGR)
    
    img12 = r_unha(img_pre,img_oc)
    img22 = r_fundo(img_pre,img_oc)
    
        
    img1 = cv2.vconcat([img_pre, img12])
    img2 = cv2.vconcat([img_oc, img22])
    
    img_out = cv2.hconcat([img1, img2])
    
    cv2.imwrite( image[2] , img_out)
   
    return [ len(np.where( openingclosing[:,:] == 0 )[0]),
           len(np.where( im_bin[:,:] == 0 )[0]) ]
    
    
    


if __name__ == '__main__':
    
    inputpath = '../pre-processing/data/'
    binarypath = '../segmentation/data/'
    outputpath = './data/'
    
    images = []

    for currentpath, folders, files in os.walk(inputpath):
        rel = os.path.relpath(currentpath,inputpath)
        bina = os.path.join(binarypath,rel)
        dest = os.path.join(outputpath,rel)
        if not os.path.exists(bina):
            print(bina + " do not exists!")
            assert False
        if not os.path.exists(dest):
            os.makedirs(dest)

        
        files.sort();
        fidx = 0
        for file in files:        
            fi = os.path.join(currentpath, file)
            fb = os.path.join(bina, Path(file).with_suffix('.png'))
            fo = os.path.join(dest, Path(file).with_suffix('.png'))
            if os.path.isfile(fi) and os.path.isfile(fb) :
                if fi.endswith('.png') and fb.endswith('.png'):
                    pe, dia = rel.split('/')
                    images.append([ fi, fb, fo, pe, dia, fidx ])
                else:
                    print("ERRO 1")
                    assert False
            else:
                print("ERRO 2")
                assert False
            fidx = fidx + 1            
     
    med = []
    for image in images:
        print(image[0])
        [s1, s2] = proc(image)
        med.append([os.path.basename(image[2]), image[3], image[4], image[5], s1, s2])
    
    with open(os.path.join(outputpath,'data.csv'), 'w') as csvfile:   
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['filename','ID','day','finger','pixels', 'raw'])
        csvwriter.writerows(med)
    
    print( "Concluido." )