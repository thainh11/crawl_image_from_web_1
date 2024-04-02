import urllib.request
from threading import Thread
import time
import requests
import random
import os

class DownloadImagesFromUrls():
    def __init__(self, nthreads, urls, destinate_folder):
        self.nthreads = nthreads
        self.urls = urls
        self.n = len(urls)
        self.destinate_folder = destinate_folder
    
    def download_url(self, start, end):
        for i in range(start, end):
            a = random.random()
            try:
                urllib.request.urlretrieve(
                    self.urls[i], f"{self.destinate_folder}/{a}.jpg"
                )
            except:
                print(f"cannot access {self.urls[i]}")
            print(".", end=" ")
    
    def __call__(self):
        threads = []
        batch = self.n//self.nthreads
        for i in range(0, self.n, batch):
            start = i
            end = i + batch
            if end >= self.n:
                end = self.n
            threads.append(Thread(target=self.download_url, args=(start,end)))
        
        start = time.time()
        for i in range(self.nthreads):
            threads[i].start()
        for i in range(self.nthreads):
            threads[i].join()
        end = time.time()
        print(f"Time download images = {end - start:.2f}s")

def get_images_from_txts(topic_names, topics):
    for dir, names in zip(topic_names, topics):
        dir_path_images = f"images"
        dir_path_urls = f"data/{dir}/urls"
        if not os.path.exists(dir_path_images):
            os.makedirs(dir_path_images)
        txts = [name for name in os.listdir(dir_path_urls) if name.endswith(".txt")]
        for txt in txts:
            folder_txt = f"{dir_path_urls}/{txt}"
            with open(folder_txt, "r") as f:
                content_txt = f.readlines()
            folder_image = f"{dir_path_images}/{txt}"
            if not os.path.exists(folder_image[:-4]):
                os.makedirs(folder_image[:-4])
            print(folder_image[:-4])
            
            
            
            n_threads = 10
            DownloadImagesFromUrls(min(n_threads, len(content_txt)//2), content_txt, folder_image[:-4])()



animal  =  ["horse", "pig", "Alligator", "bird"]

plant = ["apple", "carrot", "flower"]

furniture = ["table", "Piano", "Bookcase", "Umbrella", "book"]

scenery = ["fireworks", "sky", "cave", "cloud"]
topic_names = ["animal", "plant", "furniture", "scenery"]
topics = [animal, plant, furniture, scenery]
get_images_from_txts(topic_names, topics)