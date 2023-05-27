# window = tk.Tk()
# window.title("Aethric Bot")
# window.geometry("640x480")

# # Create a grid layout for images
# image_grid = tk.Frame(window)
# image_grid.pack(pady=10)

# # Keep track of the number of images added
# image_count = 0

# threads: List[Tuple[Thread, Event]] = []

# # Function to handle button click event
# def button_click_remove_image(index):
#     # Destroy the image label and remove it from the grid
#     image_labels[index].destroy()
        
#     (thread, stop_flag) = threads[index]
            
#     stop_flag.set()
#     thread.join()
#     # painter.clean_window()
    
#     # Remove the reference to the image label
#     del image_labels[index]

# # Create a list to store the image labels
# image_labels = []

# # Function to handle mouse hover event
# def on_enter(event, index):
#     # Create a circular red button
#     remove_button = tk.Button(image_labels[index], text="X", bg="red", fg="white", bd=0, relief="solid", width=2, command = lambda: button_click_remove_image(index))

#     # Position the button in the top right corner of the image label
#     remove_button.place(x=0, y=0)

# # Function to handle mouse leave event
# def on_leave(event, index):
#     # Remove the circular red button when the mouse leaves the image label
#     for widget in image_labels[index].winfo_children():
#         widget.destroy()
        
# # Define a callback function for the button click event
# def button_click(camera: DXCamera):
#     global image_count
    
#     if image_count >= 10:
#         return
    
#     # Open a file chooser dialog and allow the user to select image files
#     filepath = filedialog.askopenfilename(filetypes=[("Image File", "*.jpg;*.jpeg;*.png")])
    
#     if filepath:
#         templateImageMat = cv2.imread(filepath)

#         stop_flag = Event()
#         thread = threading.Thread(None, lambda: process_frame(camera, templateImageMat, stop_flag))
#         threads.append((thread, stop_flag))
#         thread.start()
        
#         # Convert the image to Tkinter PhotoImage format
#         image = Image.open(filepath)
        
#         image = image.resize((64, 64), Image.ANTIALIAS)

#         photo = ImageTk.PhotoImage(image)

#         # Create a label in the window to display the image
#         image_label = tk.Label(image_grid, image=photo)
#         image_label.image = photo  # Store a reference to avoid garbage collection
#         image_label.grid(row=image_count // 5, column=image_count % 5)
        
#         # Bind mouse hover events to the image label
#         image_label.bind("<Enter>", lambda event, index=image_count: on_enter(event, index))
#         image_label.bind("<Leave>", lambda event, index=image_count: on_leave(event, index))

#         # Add the image label to the list
#         image_labels.append(image_label)

#         # Increment the image count
#         image_count += 1        

# # Create a button in the Tkinter window
# button = tk.Button(window, text="Select Image", command = lambda: button_click(camera), relief="solid", bd=2, padx=10, pady=5, borderwidth=2, font=("Arial", 12))
# button.pack(pady=10)

# # Set the button border to rounded
# button.configure(border=4, relief="solid", borderwidth=4, highlightthickness=0, highlightbackground="#000000")

# # Center the button at the bottom
# window.update()
# button.place(relx=0.5, rely=1, anchor="s")