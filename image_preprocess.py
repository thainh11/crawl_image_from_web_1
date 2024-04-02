import os
from PIL import Image
import numpy as np
import warnings
warnings.filterwarnings("ignore", "(Possibly)?corrupt EXIF data", UserWarning)
Image.MAX_IMAGE_PIXELS = None

def processing_data(images_path):
    dic_categories = {"animal": [], "plant":[], "furniture":[], "scenery":[]}
    count = 0
    for folder in os.listdir(images_path):
        if folder.split("_")[0] in dic_categories:
            path = images_path + folder
            list_dir = [path + "/" + name for name in os.listdir(path) if name.endswith((".jpg", ".png", ".jpeg"))]
            for p in list_dir:
                try:
                    img = Image.open(p)
                    img.verify()
                    img = Image.open(p)
                    if img.width < 10:
                        print("Image too small: ", p)
                        os.remove(p)
                    
                    img = np.asarray(img)
                    if img.shape[2] != 3:
                        os.remove(p)
                except Exception as e:
                    print(e)
                    count += 1
                    print("error: ", p)
                    os.remove(p)

processing_data(images_path="D:/Work/crawl_image_from_web/images/")