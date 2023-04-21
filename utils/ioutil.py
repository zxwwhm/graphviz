import os 
import json
import numpy as np

def _makedirs(save_path):
    """确保目录创建"""
    if not save_path:
        return
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))


def write_txt(data_list, save_path, mode='w'):
    _makedirs(save_path)
    with open(save_path, mode) as f:
        for item in data_list:
            if isinstance(item, (tuple, list)):
                line_format = "{} " * len(item)
                line_format = line_format.strip() + '\n'
                line_format = line_format.format(*item)
            else:
                line_format = item.strip() + '\n'
            
            f.write(line_format)


def write_json(data, save_path, mode='w'):
    _makedirs(save_path)
    with open(save_path, mode) as f:
        json.dump(data, f)


def read_json(save_path):
    res = []
    if not os.path.exists(save_path): return res
    with open(save_path, 'r') as f:
        res = json.load(f)
    return res


def read_txt(save_path, sep=' '):
    data_list = []
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            for line in f.readlines():
                segs = line.split(sep)
                segs = [seg.strip() for seg in segs]
                data_list.append(segs)
    return data_list


def read_npy(save_path):
    return np.load(save_path)


def load_images(img_dirs, fullpath=True):
    # 获取指定目录的图片
    img_paths = []
    if isinstance(img_dirs, str):
        img_dirs = [img_dirs]
    for img_dir in img_dirs:
        img_paths.extend([os.path.join(img_dir, filename) if fullpath else filename
                          for filename in os.listdir(img_dir) if filename.lower().endswith((".jpg", '.jpeg', '.png'))])

    return img_paths


def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


