import albumentations as A
import cv2
import os, glob

in_dir = './data'
out_dir = './output'

path = ['/home/pytholic/Desktop/Projects/window_detection/scripts/new_scripts/albumentations_test/data/0_left_frame_1220.jpg',
'/home/pytholic/Desktop/Projects/window_detection/scripts/new_scripts/albumentations_test/data/12_left_frame_1070.jpg',
'/home/pytholic/Desktop/Projects/window_detection/scripts/new_scripts/albumentations_test/data/2_right_frame_600.jpg']

# Declare an augmentation pipeline
transform = A.Compose([
    #A.Equalize(mode= 'cv', by_channels=False, p=1.0)
    #A.RandomBrightnessContrast(p=1.0),
    #A.RGBShift(p=1.0),
    #A.HueSaturationValue(p=1.0),
    #A.ChannelShuffle(p=1.0),
    #A.CLAHE(p=1.0)
    #A.RandomGamma(p=1.0)
    #A.ToGray(p=1.0)
    #A.ChannelDropout(p=1.0)
    #A.MedianBlur(p=1.0),
    #A.ColorJitter(p=1.0),
    #A.GaussNoise(p=1.0),
    A.HistogramMatching(reference_images = path, p=1.0)
    #A.HorizontalFlip(p=1.0)
    #A.PixelDropout(p=1.0)
])

for path in glob.glob(in_dir + '/*.jpg'):
    name = path.split('/')[-1].split('.')[0]
    image = cv2.imread(path)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    transformed = transform(image=image)
    transformed_image = transformed["image"]
    cv2.imwrite(out_dir + '/' + name + 'augmented.jpg', transformed_image)



# # Read an image with OpenCV and convert it to the RGB colorspace
# image = cv2.imread("image.jpg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# # Augment an image
# transformed = transform(image=image)
# transformed_image = transformed["image"]
