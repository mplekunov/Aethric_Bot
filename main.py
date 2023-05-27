import threading
from threading import Event
from threading import Thread

import time
from typing import List, Tuple

from cv2 import Mat

from imageDetector import ImageDetector
from areaPainter import AreaPainter

import cv2

import dxcam
from dxcam import DXCamera

import tkinter as tk
from tkinter import filedialog

def draw_image_borders(imageAreas):
    painter = AreaPainter("RenderWindow")
    painter.clean_window()
    
    threads = []
    for area in imageAreas:            
        thread = threading.Thread(None, lambda: painter.draw_border(area))
        threads.append(thread)
            
        thread.start()       

    for thread in threads:
        thread.join() 
        
def process_frame(camera: DXCamera, templateImageMat: Mat, stop_flag: Event):
    while not stop_flag.is_set(): 
        frame = camera.get_latest_frame()

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frameMat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
        imageAreas = ImageDetector().detectImageAreas(frameMat, templateImageMat, 0.60, False)
        draw_image_borders(imageAreas)
    
        time.sleep(1)
            
camera = dxcam.create()
camera.start(target_fps=50)

window = tk.Tk()
window.title("Aethric Bot")
window.geometry("640x480")

threads: List[Tuple[Thread, Event]] = []

# Define a callback function for the button click event
def button_click(camera: DXCamera):
    # Open a file chooser dialog and allow the user to select image files
    filepath = filedialog.askopenfilename(filetypes=[("Image File", "*.jpg;*.jpeg;*.png")])
    templateImageMat = cv2.imread(filepath)

    stop_flag = Event()
    thread = threading.Thread(None, lambda: process_frame(camera, templateImageMat, stop_flag))
    threads.append((thread, stop_flag))
    thread.start()

# Create a button in the Tkinter window
button = tk.Button(window, text = "Select Images", command = lambda: button_click(camera))
button.pack()

window.mainloop()

# Clean up
for (thread, stop_flag) in threads:
    stop_flag.set()
    thread.join()

camera.stop()
