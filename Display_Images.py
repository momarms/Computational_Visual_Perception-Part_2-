import os
import matplotlib.pyplot as plt
from matplotlib.image import imread

def display_images(folder1, folder2):
    for i in range(1, 5001):
        img_path1 = os.path.join(folder1, f"{i}.png")
        img_path2 = os.path.join(folder2, f"{i}.png")

        if os.path.exists(img_path1) and os.path.exists(img_path2):
            image1 = imread(img_path1)
            image2 = imread(img_path2)

            # Display images side by side
            plt.subplot(1, 2, 1)
            plt.imshow(image1, cmap = 'gray')
            plt.title(f'Image {i} from {folder1}')

            plt.subplot(1, 2, 2)
            plt.imshow(image2, cmap = 'gray')
            plt.title(f'Image {i} from {folder2}')

            # Show close the image after 1 second
            plt.show(block = False)
            plt.pause(1)
            plt.close()

if __name__ == "__main__":
    folder_path1 = "cloth"
    folder_path2 = "distances"

    display_images(folder_path1, folder_path2)