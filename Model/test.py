from __future__ import print_function
import os
import numpy as np
import cv2

#data_dir = 'drive/My Drive/raw/'
data_dir = './raw/'

image_rows = 64   # 저장할 영상 높이
image_cols = 64    # 저장할 영상 너비
skip = 1            # 건너뛸 영상 갯수

// 다음 프로그램에서 mask 부분 없애야 함.
def read_imgs(img_path, mask_path):

    # img_path 폴더 안에 있는 모든 파일의 이름을 images 에 넣는다.
    images = os.listdir(img_path)
    total = len(images)  # 파일 개수 = 영상갯수

    mask_images = os.listdir(mask_path)
    mask_total = len(mask_images)

    imgs = np.zeros((total//skip, image_rows, image_cols), dtype=np.uint8)
    mask_imgs = np.zeros((mask_total//skip, image_rows, image_cols), dtype=np.uint8)

    if(total != mask_total):
        print ('Error in number of images and mask_images')
        return imgs,mask_imgs

    i = 0
    print('Making numpy array from images...')
    for image_name in images:
      if i % skip == 0 and i//skip < total//skip :  # skip 마다 영상 읽고 추가
        print (i, i//skip)

        # 영상 폴더 이름과 파일 이름을 연결하여 파일을 읽는다
        img = cv2.imread(os.path.join(img_path, image_name), cv2.IMREAD_GRAYSCALE)
        tmp = cv2.resize(img, (image_cols, image_rows), interpolation=cv2.INTER_CUBIC)
        imgs[i//skip] = tmp

        # 마스크 영상 폴더 이름과 파일 이름을 연결하여 파일을 읽는다
        img = cv2.imread(os.path.join(mask_path, image_name), cv2.IMREAD_GRAYSCALE)
        tmp = cv2.resize(img, (image_cols, image_rows), interpolation=cv2.INTER_CUBIC)
        mask_imgs[i//skip] = tmp
      i += 1
    print(str(total//skip) + '  Loading done.')

    return imgs, mask_imgs

def vis_img_mask(imgs, mask_imgs, wn):

    size = int(imgs.shape[0]/5)
    print (imgs.shape[0], size)
    w = imgs.shape[2]
    h = imgs.shape[1]
    t_img = np.zeros((2*h,6*w), np.uint8)
    for i in range (5):
        t_img[0:h,i*w:i*w+w] = imgs[i*size]
        t_img[h:h+h,i*w:i*w+w] = mask_imgs[i*size]
    t_img[0:h,5*w:5*w+w] = imgs[imgs.shape[0]-1]
    t_img[h:h+h,5*w:5*w+w] = mask_imgs[imgs.shape[0]-1]

    #from google.colab.patches import cv2_imshow
    #cv2_imshow(t_img)
    cv2.imshow(wn+' img', t_img)
    cv2.moveWindow(wn+' img', 20, 0)
    cv2.waitKey(0)

def create_train_data():

    imgs, mask_imgs = read_imgs(data_dir+'train', data_dir+'train_mask')
    np.save('imgs_train.npy', imgs)
    np.save('imgs_mask_train.npy', mask_imgs)

    vis_img_mask(imgs, mask_imgs, 'train')

def create_test_data():

    imgs, mask_imgs = read_imgs(data_dir+'test', data_dir+'test_mask')
    np.save('imgs_test.npy', imgs)
    np.save('imgs_mask_test.npy', mask_imgs)

    vis_img_mask(imgs, mask_imgs, 'test')

def load_train_data():
    imgs_train = np.load('imgs_train.npy')
    imgs_mask_train = np.load('imgs_mask_train.npy')
    return imgs_train, imgs_mask_train

def load_test_data():
    imgs_test = np.load('imgs_test.npy')
    imgs_mask_test = np.load('imgs_mask_test.npy')
    return imgs_test, imgs_mask_test

if __name__ == '__main__':
    create_train_data()
    create_test_data()