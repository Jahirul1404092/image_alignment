# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:14:41 2023

@author: Jahirul_Islam
"""
import cv2
import numpy as np
import glob
import os
import argparse


def imagerotate(image, angle=0):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def find_ROI(image_copy, contours, rotate=False, padding=50, height_factor=5.03):
    print(padding, height_factor)
    paddingX=padding
    paddingY=padding*height_factor
    arealst=list()
    for contour in contours:
        arealst.append(cv2.contourArea(contour))
        arealst.sort()
    outputimage=image_copy
    for contour in contours:
        area = cv2.contourArea(contour)
        if area ==arealst[-2]:
            print(area)
            
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
            print('angle: ', angle)
            # Calculate the starting and ending points for the horizontal line
            start_point = (0, int(y))
            end_point = (image_copy.shape[1], int(y))
            if(rotate==True):
                rotating_angle = angle-90
                outputimage = imagerotate(image_copy, rotating_angle)
            else:
                best=contour
                rect = cv2.minAreaRect(best)
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                pts = box.reshape((-1, 1, 2))
                isClosed = True
                box=[box[1],box[2],box[3],box[0]]
                box = [
                    [box[0][0] - paddingX, box[0][1] - paddingY],
                    [box[1][0] + paddingX, box[1][1] - paddingY],
                    [box[2][0] + paddingX, box[2][1] + paddingY],
                    [box[3][0] - paddingX, box[3][1] + paddingY]]
                    
                print("box",  box)
                pts_src = np.array(box, np.float32)
                width = max([np.linalg.norm(pts_src[2] - pts_src[3]), np.linalg.norm(pts_src[0] - pts_src[1])])
                height = max([np.linalg.norm(pts_src[1] - pts_src[2]), np.linalg.norm(pts_src[0] - pts_src[3])])
                pts_dst = np.array([[0, 0], [width-0, 0], [width-0, height-0], [0, height-0]], np.float32)
                M = cv2.getPerspectiveTransform(pts_src, pts_dst)
                outputimage = cv2.warpPerspective(image_copy, M, (int(width),int(height)))   
    return outputimage



if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--padding", type=int, default=50, help="Padding pixel for making an image square")
    parser.add_argument("--height_factor", type=float, default=5.03, help="height_factor padding pixel for making an image square")
    parser.add_argument("--input", type=str, default="data\\001", help="give the dataset path")
    parser.add_argument("--output", type=str, default="results\\", help="give the dataset path")
    parser.add_argument("--min_threshold", type=int, default=100, help="give the min threshold value for gray scal convertion")
    parser.add_argument("--max_threshold", type=int, default=250, help="give the max threshold value for gray scal convertion")
    args = parser.parse_args()
    
    padding = args.padding
    height_factor = args.height_factor
    output_dir = args.output
    dataset_path = args.input
    min_threshold = args.min_threshold
    max_threshold = args.max_threshold
    print(output_dir, dataset_path)
    best = None
    output_dir1=output_dir+"\\"
    
    for filepath in glob.glob(dataset_path+"\\**\\*.JPG", recursive=True):
        #print(filepath)
        index=filepath.rfind('\\')
        output_dir2=filepath[filepath.find('\\')+1:filepath.rfind('\\')+1]
        output_dir=output_dir1+output_dir2
        #print(output_dir)
        image_name=filepath[index+1:]
        os.makedirs(output_dir, exist_ok=True)
    
        image = cv2.imread(filepath)
        #image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)) )
        
        # convert the image to grayscale format
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # apply binary thresholding
        ret, thresh = cv2.threshold(img_gray, min_threshold, max_threshold, cv2.THRESH_BINARY)
        
        # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        #print(padding, height_factor)
        
        image = find_ROI(image, contours, rotate=True, padding=padding, height_factor=height_factor)
        
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, min_threshold, max_threshold, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        image = find_ROI(image, contours, rotate=False, padding=padding, height_factor=height_factor)
        cv2.imwrite(output_dir+image_name, image)
    
