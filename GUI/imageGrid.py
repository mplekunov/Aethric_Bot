# Create a grid layout for images
from tkinter import Button, Frame, Label, Tk
from typing import Dict
from uuid import UUID

from PIL import ImageTk

from objectTracker import ObjectTracker

class ImageGrid(object):
    def __init__(self, window: Tk, tracker: ObjectTracker):
        self._imageMap: Dict[UUID, Label] = {}        
        self._image_count = 0

        self._image_grid = Frame(window)
        self._image_grid.pack(pady=10)
        
        self._tracker = tracker
    
    # Function to handle button click event
    def _button_click_remove_image(self, uuid, tracker: ObjectTracker):    
        # Destroy the image label and remove it from the grid
        # Remove the reference to the image label
        self._imageMap.pop(uuid).destroy()

        tracker.stop_tracking(uuid) 

        self._image_count -= 1        

    # Function to handle mouse hover event
    def _on_enter(self, event, uid):
        # Create a circular red button
        remove_button = Button(self._imageMap[uid], text="X", bg="red", fg="white", bd=0, relief="solid", width=2, command = lambda: self._button_click_remove_image(uid, self._tracker))

        # Position the button in the top right corner of the image label
        remove_button.place(x=0, y=0)

    # Function to handle mouse leave event
    def _on_leave(self, event, uid):
        # Remove the circular red button when the mouse leaves the image label
        for widget in self._imageMap[uid].winfo_children():
            widget.destroy()

    def add_image(self, uid: UUID, image: ImageTk.PhotoImage):
        # Create a label in the window to display the image
        image_label = Label(self._image_grid, image=image)
        image_label.image = image  # Store a reference to avoid garbage collection
        image_label.grid(row=self._image_count // 5, column=self._image_count % 5)
        
        # Bind mouse hover events to the image label
        image_label.bind("<Enter>", lambda event, uid=uid: self._on_enter(event, uid))
        image_label.bind("<Leave>", lambda event, uid=uid: self._on_leave(event, uid))
        
        # Add the image label to the list
        self._imageMap[uid] = image_label
        
        # Increment the image count
        self._image_count += 1
    
    def get_image_count(self):
        return self._image_count