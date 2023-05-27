from typing import Dict
from uuid import UUID

from camera import Camera

from imageDetector import ImageDetector
from areaPainter import AreaPainter

import cv2

import tkinter as tk
from tkinter import Label, filedialog

from PIL import ImageTk, Image

from objectFinder import ObjectTracker

painter = AreaPainter("RenderWindow")
imageDetector = ImageDetector()
camera = Camera()
objectFinder = ObjectTracker(painter, imageDetector, camera)

window = tk.Tk()
window.title("Aethric Bot")
window.geometry("640x480")

# Create a grid layout for images
image_grid = tk.Frame(window)
image_grid.pack(pady=10)

# Keep track of the number of images added
image_count = 0

imageMap: Dict[UUID, Label] = {}

# Function to handle button click event
def button_click_remove_image(uuid):
    global image_count
    
    # Destroy the image label and remove it from the grid
    # Remove the reference to the image label
    imageMap.pop(uuid).destroy()
    
    objectFinder.stop_tracking(uuid) 

    image_count -= 1

# Function to handle mouse hover event
def on_enter(event, uid):
    # Create a circular red button
    remove_button = tk.Button(imageMap[uid], text="X", bg="red", fg="white", bd=0, relief="solid", width=2, command = lambda: button_click_remove_image(uid))

    # Position the button in the top right corner of the image label
    remove_button.place(x=0, y=0)

# Function to handle mouse leave event
def on_leave(event, uid):
    # Remove the circular red button when the mouse leaves the image label
    for widget in imageMap[uid].winfo_children():
        widget.destroy()

# Define a callback function for the button click event
def button_click():
    global image_count
    
    if image_count >= 10:
        return
    
    # Open a file chooser dialog and allow the user to select image files
    filepath = filedialog.askopenfilename(filetypes=[("Image File", "*.jpg;*.jpeg;*.png")])
    
    if filepath:
        templateImageMat = cv2.imread(filepath)

        uid = objectFinder.track_object(templateImageMat, 1)
        
        # Convert the image to Tkinter PhotoImage format
        image = Image.open(filepath)
        
        image = image.resize((64, 64), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        # Create a label in the window to display the image
        image_label = tk.Label(image_grid, image=photo)
        image_label.image = photo  # Store a reference to avoid garbage collection
        image_label.grid(row=image_count // 5, column=image_count % 5)
        
        # Bind mouse hover events to the image label
        image_label.bind("<Enter>", lambda event, uid=uid: on_enter(event, uid))
        image_label.bind("<Leave>", lambda event, uid=uid: on_leave(event, uid))

        # Add the image label to the list
        imageMap[uid] = image_label

        # Increment the image count
        image_count += 1        

# Create a button in the Tkinter window
button = tk.Button(window, text="Select Image", command=button_click, relief="solid", bd=2, padx=10, pady=5, borderwidth=2, font=("Arial", 12))
button.pack(pady=10)

# Set the button border to rounded
button.configure(border=4, relief="solid", borderwidth=4, highlightthickness=0, highlightbackground="#000000")

# Center the button at the bottom
window.update()
button.place(relx=0.5, rely=1, anchor="s")

window.mainloop()

# Clean up
for uid in imageMap.keys():
    objectFinder.stop_tracking(uid)
