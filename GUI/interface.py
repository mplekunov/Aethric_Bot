from tkinter import Button, Tk, filedialog

import cv2

from PIL import Image
from PIL import ImageTk

from GUI.imageGrid import ImageGrid
from objectTracker import ObjectTracker

class Interface(object):
    def __init__(self, tracker: ObjectTracker):
        # Main window information
        self._window = Tk()
        
        self._window.title("Aethric Bot")
        self._window.geometry("640x480")

        self._image_grid = ImageGrid(self._window, tracker)

        # Create a button in the Tkinter window
        button = Button(self._window, text="Select Image", command= lambda: self._button_click(tracker), relief="solid", bd=2, padx=10, pady=5, borderwidth=2, font=("Arial", 12))
        button.pack(pady=10)

        # Set the button border to rounded
        button.configure(border=4, relief="solid", borderwidth=4, highlightthickness=0, highlightbackground="#000000")

        button.place(relx=0.5, rely=1, anchor="s")

        # Center the button at the bottom
        self._window.update()            

    # Define a callback function for the button click event
    def _button_click(self, tracker: ObjectTracker):
        if self._image_grid.get_image_count() > 10:
            return
        
        # Open a file chooser dialog and allow the user to select image files
        filepath = filedialog.askopenfilename(filetypes=[("Image File", "*.jpg;*.jpeg;*.png")])

        if filepath:
            templateImageMat = cv2.imread(filepath)

            uid = tracker.track_object(templateImageMat, 1)

            # Convert the image to Tkinter PhotoImage format
            image = Image.open(filepath)

            image = image.resize((64, 64), Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)

            self._image_grid.add_image(uid, photo)
    
    def run_interface(self):
        self._window.mainloop()