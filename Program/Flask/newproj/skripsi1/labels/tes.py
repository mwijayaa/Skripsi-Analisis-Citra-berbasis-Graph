import os

image_names = os.listdir('./images')
print(image_names)
print(type(image_names))
# return render_template("gallery.html", image_names=image_names)