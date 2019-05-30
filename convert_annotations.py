#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
from scipy.io import loadmat

annopath='D:/Private Manager/Personal File/uOttawa/Lab works/2019 summer/caltech_dataset/annotations'

all_obj = 0
data = {}

folders=[os.path.join(annopath,'set'+str(i).zfill(2)) for i in range(1,2)] # debug set
#folders=[os.path.join(annopath,'set'+str(i).zfill(2)) for i in range(6)] # training set
#folders=[os.path.join(annopath,'set'+str(i).zfill(2)) for i in range(6,11)] # testing set

for dname in folders:#set[00-09]
    set_name = os.path.basename(dname)
    for anno_fn in sorted(glob.glob('{}/*.vbb'.format(dname))):#*.vbb
        vbb = loadmat(anno_fn)
        nFrame = int(vbb['A'][0][0][0][0][0])
        objLists = vbb['A'][0][0][1][0]
        maxObj = int(vbb['A'][0][0][2][0][0])
        objInit = vbb['A'][0][0][3][0]
        objLbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
        objStr = vbb['A'][0][0][5][0]
        objEnd = vbb['A'][0][0][6][0]
        objHide = vbb['A'][0][0][7][0]
        altered = int(vbb['A'][0][0][8][0][0])
        log = vbb['A'][0][0][9][0]
        logLen = int(vbb['A'][0][0][10][0][0])

        video_name = os.path.splitext(os.path.basename(anno_fn))[0]
# =============================================================================
#         data[set_name][video_name]['nFrame'] = nFrame
#         data[set_name][video_name]['maxObj'] = maxObj
#         data[set_name][video_name]['log'] = log.tolist()
#         data[set_name][video_name]['logLen'] = logLen
#         data[set_name][video_name]['altered'] = altered
# =============================================================================
        

        n_obj = 0
        for frame_id, obj in enumerate(objLists):
            imgname='{}_{}_{}.jpg'.format(set_name,video_name,str(frame_id).zfill(5))
            data[imgname] = {}
            data[imgname]['annotations']=[]
            data[imgname]['name']=imgname
            data[imgname]['width']=640
            data[imgname]['height']=480
            
            if len(obj) > 0:
                for objid, pos, occl, lock, posv in zip(
                        obj['id'][0], obj['pos'][0], obj['occl'][0],
                        obj['lock'][0], obj['posv'][0]):
                    keys = obj.dtype.names
                    objid = int(objid[0][0]) - 1  # MATLAB is 1-origin
                    pos = pos[0].tolist()
                    occl = int(occl[0][0])
                    lock = int(lock[0][0])
                    posv = posv[0].tolist()
                    
                    anno={}                    
                    anno['label'] = str(objLbl[objid])
                    if anno['label']!= 'person':
                        continue
                    
                    anno['category']=''
                    anno['id']=objid
                    anno['shape']=['box',1]
                    anno['x']=pos[0]
                    anno['y']=pos[1]
                    anno['width']=pos[2]
                    anno['height']=pos[3]
                    
                    data[imgname]['annotations'].append(anno)
                    n_obj += 1

        print(dname, anno_fn, n_obj)
        all_obj += n_obj

print('Number of objects:', all_obj)
json.dump(data, open(os.path.join(annopath,'caltech_annotation_VIVA_.json'), 'w'),sort_keys=True, indent=4)
