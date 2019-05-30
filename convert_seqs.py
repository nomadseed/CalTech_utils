#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import cv2 as cv


def save_img(dname, fn, i, frame):
    cv.imwrite('{}/{}_{}_{}.jpg'.format(
        out_dir, os.path.basename(dname),
        os.path.basename(fn).split('.')[0], str(i).zfill(5)), frame)

seqpath='D:/Private Manager/Personal File/uOttawa/Lab works/2019 summer/caltech_dataset/seqs'
out_dir = 'D:/Private Manager/Personal File/uOttawa/Lab works/2019 summer/caltech_dataset/images'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
for dname in sorted(glob.glob(os.path.join(seqpath,'set*'))):
    for fn in sorted(glob.glob('{}/*.seq'.format(dname))):#*.seq
        cap = cv.VideoCapture(fn)
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            save_img(dname, fn, i, frame)
            i += 1
        print(fn)
