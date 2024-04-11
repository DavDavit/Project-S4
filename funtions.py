import requests
import os
from tkinter import Tk, Canvas, PhotoImage, Scrollbar
from PIL import Image, ImageTk


def create_folder(filename):
    if not os.path.exists(filename):
        os.makedirs(filename)
        

def getImage(ra, dec, scale, opt, image_name):
    url = f'http://skyserver.sdss.org/dr18/SkyServerWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale={scale}&width=800&height=800&opt={opt}'
    response = requests.get(url)
    create_folder('images')
    if response.status_code == 200:
        with open(os.path.join('images', image_name + '.jpg'), "wb") as f:
            f.write(response.content)
        print("Image saved successfully.")

def getImageFromRange(ra_min, ra_max, dec_min, dec_max, scale, step):
    ra = ra_min
    while ra < ra_max :
        dec = dec_min
        while dec < dec_max:
            getImage(ra, dec, scale, 'L', "img_" + str(ra) +"_" + str(dec))
            dec+=step
        ra += step


def display_images(ra_min, ra_max, dec_min, dec_max, scale, step):
    folder_path='images'
    getImageFromRange(ra_min, ra_max, dec_min, dec_max, scale, step)

    # Create a Tkinter window
    root = Tk()
    root.title("Image Viewer")
   
    images = [file for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
    num_images = len(images)

    # Calculate the number of rows and columns for the grid layout
    num_cols = 3
    num_rows = (num_images + num_cols - 1) // num_cols

    # Create a canvas to display the images
    canvas = Canvas(root, width=num_cols*200 + (num_cols-1)*10, height=num_rows*200 + (num_rows-1)*10)
    canvas.pack()

    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to scroll vertically
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.config(yscrollcommand=scrollbar.set)

    # Function to update scrollregion
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_configure)

    # List to hold references to PhotoImage objects
    photo_images = []

    # Load and display each image on the canvas
    for i, image_file in enumerate(images):
        row = i // num_cols
        col = i % num_cols

        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        image.thumbnail((200, 200))  # Resize the image to fit the canvas
        photo = ImageTk.PhotoImage(image)
        photo_images.append(photo)  # Store reference to PhotoImage object

        # Calculate coordinates with gap
        x = col * 210 + 100
        y = row * 210 + 100

        canvas.create_image(x, y, image=photo)

    root.mainloop()

# Example usage:
display_images(220.525575754, 230.525575754, 50.745853761, 60.745853761,  0.3, 3)
