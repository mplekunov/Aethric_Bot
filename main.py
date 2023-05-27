from ast import Set
import threading
import time

import heapq

from imageDetector import ImageDetector

import cv2
import numpy as np

import dxcam

from areaPainter import AreaPainter

def draw_image_identifiers(imageAreas):
    painter = AreaPainter("RenderWindow")
    painter.clean_window()
    
    threads = []
    for area in imageAreas:            
        thread = threading.Thread(None, lambda: painter.draw_identifier(area))
        threads.append(thread)
            
        thread.start()       

    for thread in threads:
        thread.join()    
    
# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
 
# Resize this window
cv2.resizeWindow("Live", 480, 270)

camera = dxcam.create()
camera.start(target_fps=50)

while True: 
    frame = camera.get_latest_frame()
 
    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    templateImage = cv2.imread("template-cleaned.png")
    imageAreas = ImageDetector().detectImageAreas(frame, templateImage, 0.60, False)
     
    draw_image_identifiers(imageAreas)
    # Optional: Display the recording screen
    # cv2.imshow('Live', resultImage)
     
    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break
    
    time.sleep(1)
    
camera.stop()

# Destroy all windows
cv2.destroyAllWindows()
