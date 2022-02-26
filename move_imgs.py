import os
import shutil
import numpy as np

np.random.seed(10)

main_repo = r'C:\Users\cdelannoy\OneDrive - Mathematica\Documents\S1_switzerland\processed'
img_repo = os.path.join(main_repo, r'20180128_22')
label_repo = os.path.join(main_repo, r'20180128_22_outlines_clipped')

train_repo = r'C:\Users\cdelannoy\Repos\unet\data\avy\train'
train_label = os.path.join(train_repo, r'label')
train_img = os.path.join(train_repo, r'image')

test_repo = r'C:\Users\cdelannoy\Repos\unet\data\avy\test'
test_label = os.path.join(test_repo, r'label')

# start with shapefiles (masks)
label_f = [f for f in os.listdir(label_repo) if f.endswith('._shapefile.TIF')]
## divide into training and testing dataset
nums = np.ones(len(label_f))
nums[:int(0.4*len(label_f))] = 0
np.random.shuffle(nums)

label_f_train = np.array(label_f)[np.array(nums == 1)]
label_f_test = np.array(label_f)[np.array(nums == 0)]

def move_and_rename_label(filename, f_path, new_id):
    f_id = filename.split('VV')[1].split('._shapefile')[0]
    new_name = str(new_id) + '.TIF'
    new_path = os.path.join(f_path, new_name)
    shutil.copy(os.path.join(label_repo, filename), new_path)
    return f_id

train_label_ids = []
for f in range(len(label_f_train)):
    train_label_ids.append(move_and_rename_label(label_f_train[f], train_label, f))

test_label_ids = []
for f in range(len(label_f_test)):
    test_label_ids.append(move_and_rename_label(label_f_test[f], test_label, f))

textfile = open("train_ids.txt", "w")
for element in train_label_ids:
    textfile.write(element + "\n")
textfile.close()

textfile = open("test_ids.txt", "w")
for element in test_label_ids:
    textfile.write(element + "\n")
textfile.close()
# now move and rename only necessary rasters
train_img_f = []
for l in train_label_ids:
    train_img_f.append([f for f in os.listdir(img_repo) if f.endswith('VV' + l + '.TIF')])

test_img_f = []
for l in test_label_ids:
    test_img_f.append([f for f in os.listdir(img_repo) if f.endswith('VV' + l + '.TIF')])

assert len(train_img_f) == len(train_label_ids)
assert len(test_img_f) == len(test_label_ids)

for f in range(len(train_img_f)):
    new_path = os.path.join(train_img, str(f) + '.TIF')
    shutil.copy(os.path.join(img_repo, train_img_f[f][0]), new_path)

for f in range(len(test_img_f)):
    new_path = os.path.join(test_repo, str(f) + '.TIF')
    shutil.copy(os.path.join(img_repo, test_img_f[f][0]), new_path)

