import glob
import os
import numpy as np
import StringIO
import base64
import networkx as nx
import matplotlib.pyplot as plt
from numpy import genfromtxt
from skimage import io, segmentation, color
from skimage.future import graph
from networkx.algorithms import isomorphism
from flask import Flask, request, render_template, send_from_directory
from ged4py.algorithm import graph_edit_dist as ged

__author__ = 'wijaya'

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("halaman input.html")

@app.route("/input", methods=["POST"])
def process():

    # target = os.path.join(APP_ROOT, 'images/')
    # print(target)
    # if not os.path.isdir(target):
    #         os.mkdir(target)
    # else:
    #     print("Couldn't create upload directory: {}".format(target))
    # print(request.files.getlist("file"))
    if request.method == 'POST':
        if request.form['submit'] == 'Segment':
            for upload in request.files.getlist("file"):
                print(upload)
                print("{} is the file name".format(upload.filename))
                filename = upload.filename

            
            filename = filename.encode('utf-8')
            filename = 'static/{}'.format(filename)
            print(filename)
            print(type(filename))
            img = io.imread(filename)
            label = segmentation.felzenszwalb(img, min_size=290 )
            bg = io.imread('blank.jpg')
            out = color.label2rgb(label, bg, kind='overlay')
            sg = 'segmen.png'
            pelot = StringIO.StringIO()
            plotku = plt.imshow(out)
            plt.savefig(pelot, format='png')
            pelot.seek(0)
            plot_url = base64.b64encode(pelot.getvalue())
            return render_template("segmentation.html", labels = label, plot_url = plot_url)

        else:
            for upload in request.files.getlist("file"):
                print(upload)
                print("{} is the file name".format(upload.filename))
                filename = upload.filename

            print(filename)
            filename = filename.encode('utf-8')
            filename = 'static/{}'.format(filename)
            print(filename)
            print(type(filename))
            path1 = 'images/'
            path2 = 'graph/'
            imgFile = []
            graphFile = []


            for filename1 in glob.glob(os.path.join(path1, '*.jpg')):
                imgFile.append(filename1)

            for filename2 in glob.glob(os.path.join(path2, '*.gpickle')):
                graphFile.append(filename2)

            matchedList = []
            img = io.imread(filename)
            label = segmentation.felzenszwalb(img, min_size=290 )
            print(label)
            g1 = graph.rag_mean_color(img, label, connectivity=2, mode='distance')
            for i in range(len(graphFile)):
                g2 = nx.read_gpickle(graphFile[i])
                gm = isomorphism.GraphMatcher(g1,g2)
                if(gm.is_isomorphic()): # isomorphism
                # if(ged.compare(g1,g2,False)) <= 8:
                    matchedList.append(imgFile[i])

            newList = []
            for i in range(len(matchedList)):
                fl = matchedList[i].replace("images\\","")
                newList.append(fl)

            n = len(newList)

            return render_template("halaman output.html", image_names=newList, jumlah=n)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/output')
def get_gallery():
    image_names = ['img001.jpg','img050.jpg']
    n = len(image_names)
    print(image_names)
    return render_template("halaman output.html", image_names=image_names, jumlah=n)

if __name__ == "__main__":
    app.run(port=5000, debug=True)