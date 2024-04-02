from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request
import time
from threading import Thread
import os

class GetimagesfromPages():
    def __init__(self, nthreads, npage, url_page):
        self.nthreads = nthreads
        self.npage = npage
        self.url_page = url_page
        self.result_urls = []
    
    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_images(self, url):
        soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
        urls = []
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            if self.is_valid(img_url):
                urls.append(img_url)
        return urls
    
    def main(self, start, end):
        for i in range(start, end):
            try:
                self.result_urls.extend(self.get_all_images(self.url_page + str(i)))
            except:
                pass
    
    def __call__(self):
        threads = []
        batch = self.npage//self.nthreads
        for i in range(0, self.npage, batch):
            start = i
            end = i + batch
            if end >= self.npage:
                end = self.npage + 1
            
            threads.append(Thread(target=self.main, args= (start, end)))
        
        start = time.time()
        for i in range(self.nthreads):
            threads[i].start()
        for i in range(self.nthreads):
            threads[i].join()
        end = time.time()
        print(f"Time handle pages = {end - start:.2f}s")
        return self.result_urls

def urls_to_txts(topic_names, topics, urltopic, n_page, n_threads):
    for dir, names in zip(topic_names, topics):
        dir_path_urls = f"data/{dir}/urls"
        if not os.path.exists(dir_path_urls):
            os.makedirs(dir_path_urls)
        for name in names:
            result_of_name = []
            for key in urltopic.keys():
                res = GetimagesfromPages(min(n_threads, n_page//2), n_page, urltopic[key].format(name=name))()
                if len(res) > 0:
                    res = list(set(res))
                    result_of_name.extend(res)
            print(f"{dir_path_urls}/{dir}_{name}.txt have {len(result_of_name)}images \n")
            strResult = "\n".join(result_of_name)
            with open(f"{dir_path_urls}/{dir}_{name}.txt", "w") as f:
                f.write(strResult)


animal  =  ["horse", "pig", "Alligator", "bird"]

plant = ["apple", "carrot", "flower"]

furniture = ["table", "Piano", "Bookcase", "Umbrella", "book"]

scenery = ["fireworks", "sky", "cave", "cloud"]

urltopic = {
    "freeimages": "https://www.freeimages.com/search/{name}/"
}
topic_names = ["animal", "plant", "furniture", "scenery"]
topics = [animal, plant, furniture, scenery]
n_threads = 3
n_page = 6
urls_to_txts(topic_names, topics, urltopic, n_page, n_threads)