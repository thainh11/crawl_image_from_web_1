from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

def read_image_from_path(path, size):
    im = Image.open(path).resize(size)
    return np.asarray(im, dtype=np.float32)

def folder_to_images(folder, size):
    list_dir = [folder + "/" + name for name in os.listdir(folder) if name.endswith((".jpg", ".png", ".jpeg"))]
    i = 0
    images_np = np.zeros(shape=(len(list_dir), *size, 3))
    images_path = []
    for path in list_dir:
        try:
            images_np[i] = read_image_from_path(path, size)
            images_path.append(path)
            i += 1
        except Exception:
            print("error: ", path)
            # os.remove(path)
    images_path = np.array(images_path)
    return images_np, images_path

def absolute_difference(query, X):
    axis_batch_size = tuple(range(1, len(X.shape)))
    return np.sum(np.abs(X - query), axis=axis_batch_size)

def get_l1_score(root_img_path, query_path, size):
    dic_categories = ["animal", "plant", "furniture", "scenery"]
    query = read_image_from_path(query_path, size)
    ls_path_score = []
    for folder in os.listdir(root_img_path):
        if folder.split("_")[0] in dic_categories:
            path = root_img_path + folder
            images_np, images_path = folder_to_images(path, size)
            rates = absolute_difference(query, images_np)
            ls_path_score.extend(list(zip(images_path, rates)))
    return query, ls_path_score

def plot_results(query, ls_path_score):
    plt.imshow(query/255.0)
    fig = plt.figure(figsize=(15, 15))
    columns = 5
    rows = 6
    for i, path in enumerate(sorted(ls_path_score, key=lambda x: x[1])[:30], 1):
        img = np.random.randint(10, size=(10,10))
        fig.add_subplot(rows, columns, i)
        plt.imshow(plt.imread(path[0]))
        plt.axis("off")
    plt.show()

def mean_squared_difference(query, X):
    axis_batch_size = tuple(range(1, len(X.shape)))
    return np.mean((X-query)**2, axis=axis_batch_size)

def cosine_similarity(query, X):
    axis_batch_size = tuple(range(1, len(X.shape)))
    query_norms = np.sqrt(np.sum(query**2))
    X_norm = np.sqrt(np.sum(X**2, axis=axis_batch_size))
    return np.sum(X * query, axis=axis_batch_size) / (query_norms * X_norm + np.finfo(float).eps)

# def get_cosine_similarity_score(query, X):
#     rates = cosine_similarity(query, images_np)

def correlation_coefficient(query, X):
    axis_batch_size = tuple(range(1, len(X.shape)))
    query_mean = query - np.mean(query)
    X_mean = X - np.mean(X, axis=axis_batch_size, keepdims=True)
    query_norms = np.sqrt(np.sum(query_mean**2))
    X_norm = np.sqrt(np.sum(X_mean**2, axis=axis_batch_size))
    return np.sum(X_mean * query_mean, axis=axis_batch_size) / (query_norms * X_norm + np.finfo(float).eps)


if __name__ == '__main__':
    root_img_path = "images/"
    query_path = "apple.jpg"
    size = (80,80)
    query, ls_path_score = get_l1_score(root_img_path, query_path, size)
    plot_results(query, ls_path_score)