# -*- coding: utf-8 -*-
"""Copy2(best) of Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/184ade9BpWmEWpWIM3ZISUbFcv6PpCPl-
"""

from fastai.vision import *

folder = 'cat'
file = 'cat.csv'

folder = 'lion'
file = 'lion.csv'

folder = 'tiger'
file  = 'tiger.csv'

path = Path('data/thegreatcatfamily')
dest = path/folder
dest.mkdir(parents=True, exist_ok=True)

classes = ['cat','lion','tiger']

download_images(path/file, dest, max_pics=200)

for c in classes:
    print(c)
    verify_images(path/c, delete=True, max_size=500)

np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)

data.classes

data.show_batch(rows=3, figsize=(7,8))



data.classes, data.c, len(data.train_ds), len(data.valid_ds)

learn = cnn_learner(data, models.resnet34, metrics=error_rate)

learn.fit_one_cycle(4)

learn.save('stage-1')

learn.unfreeze()

learn.lr_find()

learn.recorder.plot()

learn.fit_one_cycle(2, max_lr=slice(3e-5,3e-4))

learn.save('stage-2')

learn.load('stage-2');

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_confusion_matrix()

from fastai.widgets import *

db = (ImageList.from_folder(path)
                   .split_none()
                   .label_from_folder()
                   .transform(get_transforms(), size=224)
                   .databunch()
     )

learn_cln = cnn_learner(db, models.resnet34, metrics=error_rate)

learn_cln.load('stage-2');

ds, idxs = DatasetFormatter().from_toplosses(learn_cln)

learn.export()

img = open_image(path/'7.jpeg')
img

learn = load_learner(path)

pred_class,pred_idx,outputs = learn.predict(img)
pred_class

"""# New Section"""