from threading import Thread
import time
from typing import List

import cv2
from cv2 import Mat

import keyboard

from classes.camera import Camera

from imageDetector import ImageDetector
from GUI.areaPainter import AreaPainter
from GUI.interface import Interface

from objectTracker import ObjectTracker

painter = AreaPainter("RenderWindow")
imageDetector = ImageDetector()
camera = Camera()
tracker = ObjectTracker(painter, imageDetector, camera)

interface = Interface(tracker)
interface.run_interface()

def is_detected(camera: Camera, imageMat: Mat, threshold: float, useColors = True):
    target = camera.get_screenshot()
    
    imageAreas = imageDetector.detectImageAreas(target, imageMat, threshold, useColors)
    
    return len(imageAreas) > 0

def draw(targetMat: Mat, imageMat: Mat, threshold: float, useColors = True):    
    imageAreas = imageDetector.detectImageAreas(targetMat, imageMat, threshold, useColors)
    
    for area in imageAreas:
        painter.draw_border(area, includeConfidence=False)
    
    
tracker.cleanup()