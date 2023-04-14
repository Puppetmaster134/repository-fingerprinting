import os
from tqdm import tqdm
import numpy as np
from default_features import TOTAL_FEATURES as get_default_features
import kfp

def load_packet_sequence(filepath):
    packets = []
    with open(filepath, 'r') as f:
        for packet_str in f.readlines():
            time, size = packet_str.split('\t')
            packets.append((float(time), int(size)))
    return packets

def file_to_features(filepath):
    fbase = os.path.basename(filepath)
    ps = load_packet_sequence(filepath)
    features = get_default_features(ps)
    page_id,load_id = fbase.split('-')
    return features,int(page_id),int(load_id)

def extract_features(data_dir):
    file_list = [f for f in os.listdir(data_dir) if f.find('-') != -1]
    print(f'Found {len(file_list)} raw data files.')

    counter = {}
    x_f = []
    labels = []
    wid = []
    print('Extracting features.')
    for file in tqdm(file_list):
        features,page_id,load_id = file_to_features(os.path.join(data_dir,file))
        x_f.append(features)
        labels.append(page_id)
        wid.append(file)
        if page_id not in counter:
            counter[page_id] = 1
        else:
            counter[page_id] += 1

    return x_f, labels, wid, len(set(labels)),min(counter.values())

def save_feature_data(X, W, out_dir='./out'):
    if not os.path.isdir(out_dir):
        print(f'Creating directory {out_dir}')
        os.makedirs(out_dir)

    print(f'Storing features into {out_dir}')
    for x,w in zip(X,W):
        fname = os.path.join(out_dir, w) + '.features'
        np.savetxt(fname, x, delimiter=',')

def main():
    data_dir = '../process/pdata/'
    x_f, labels, wid, n_pages, n_loads = extract_features(data_dir)
    print(n_pages)
    print(n_loads)
    save_feature_data(x_f, wid)

if __name__ == "__main__":
    main()