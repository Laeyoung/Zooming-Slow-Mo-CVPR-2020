#!/usr/bin/env python3
import os
import os.path as osp
import glob
import logging
import numpy as np
import cv2
import torch

import utils.util as util
import data.util as data_util
import models.modules.Sakuya_arch as Sakuya_arch

import argparse
from shutil import rmtree

def zsm():
    scale = 4
    N_ot = 3 # args.N_out
    N_in = 1 + N_ot//2
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    #### model
    model_path = "/app/model.pth"
    model = Sakuya_arch.LunaTokis(64, N_ot, 8, 5, 40)

    #### extract the input video to temporary folder
    save_folder = osp.join(osp.dirname("output.mp4"), '.delme')
    save_out_folder = osp.join(osp.dirname("output.mp4"), '.hr_delme')
    util.mkdirs(save_folder)
    util.mkdirs(save_out_folder)
    error = util.extract_frames("", "input.mp4", save_folder)
    if error:
        print(error)
        exit(1)

    # temporal padding mode
    padding = 'replicate'
    save_imgs = True

    ############################################################################
    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')
    
    def single_forward(model, imgs_in):
        with torch.no_grad():
            # print(imgs_in.size()) # [1,5,3,270,480]
            b,n,c,h,w = imgs_in.size()
            h_n = int(4*np.ceil(h/4))
            w_n = int(4*np.ceil(w/4))
            imgs_temp = imgs_in.new_zeros(b,n,c,h_n,w_n)
            imgs_temp[:,:,:,0:h,0:w] = imgs_in
            model_output = model(imgs_temp)
            model_output = model_output[:, :, :, 0:scale*h, 0:scale*w]
            if isinstance(model_output, list) or isinstance(model_output, tuple):
                output = model_output[0]
            else:
                output = model_output
        return output

    model.load_state_dict(torch.load(model_path), strict=True)

    model.eval()
    model = model.to(device)
    #### zsm images
    imgs = util.read_seq_imgs(save_folder)
    select_idx_list = util.test_index_generation(False, N_ot, len(imgs))
    for select_idxs in select_idx_list:
        # get input images
        select_idx = select_idxs[0]
        imgs_in = imgs.index_select(0, torch.LongTensor(select_idx)).unsqueeze(0).to(device)
        output = single_forward(model, imgs_in)
        outputs = output.data.float().cpu().squeeze(0)            
        # save imgs
        out_idx = select_idxs[1]
        for idx,name_idx in enumerate(out_idx):
            output_f = outputs[idx,...].squeeze(0)
            if save_imgs:     
                output = util.tensor2img(output_f)
                cv2.imwrite(osp.join(save_out_folder, '{:06d}.png'.format(name_idx)), output)

    # now turn output images to video
    # generate mp4
    util.create_video("", save_out_folder, "output.mp4", 24)

    # remove tmp folder    
    rmtree(save_folder)
    rmtree(save_out_folder)
    
    #exit(0)

#if __name__ == '__main__':
#    main()
