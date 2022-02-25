import os
import shutil

main_repo = r'C:\Users\cdelannoy\OneDrive - Mathematica\Documents\S1_switzerland\processed'
img_repo = os.path.join(main_repo, r'20180128_22')
label_repo = os.path.join(main_repo, r'20180128_22_outlines_clipped')

train_repo = r'C:\Users\cdelannoy\Repos\unet\data\avy\train'
train_label = os.path.join(train_repo, r'label')
train_img = os.path.join(train_repo, r'image')

# start with shapefiles (masks)
label_f = [f for f in os.listdir(label_repo) if f.endswith('._shapefile.TIF')]

def move_and_rename_label(filename):
    f_id = filename.split('VV')[1].split('._shapefile')[0]
    new_name = f_id + '.TIF'
    new_path = os.path.join(train_label, new_name)
    shutil.copy(os.path.join(label_repo, filename), new_path)
    return f_id

label_ids = []
for f in label_f:
    label_ids.append(move_and_rename_label(f))

# now move and rename only necessary rasters
img_f = []
for l in label_ids:
    img_f.append([f for f in os.listdir(img_repo) if f.endswith('VV' + l + '.TIF')])

assert len(img_f) == len(label_ids)

for f in img_f:
    new_name = f[0].split('VV')[1]
    new_path = os.path.join(train_img, new_name)
    shutil.copy(os.path.join(img_repo, f[0]), new_path)

