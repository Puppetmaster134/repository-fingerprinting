import os
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import default_features as df

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
    page_id,load_id = fbase.split('-')
    feature_dict = {}
    mean_in, mean_out = df.average_in_out_pkt_size(ps)
    feature_dict['mean_length_in'], feature_dict['mean_length_out'] = (abs(int(mean_in)), int(mean_out))
    
    interarrival_stats = df.interarrival_maxminmeansd_stats(ps)[0]
    feature_dict['inter_mean_in'],feature_dict['inter_mean_out'],feature_dict['inter_mean_tot'] = interarrival_stats[3:6]
    # [x for x in df.interarrival_maxminmeansd_stats(ps)]
    feature_dict['unique_len_in'], feature_dict['unique_len_out'], feature_dict['unique_len_total'] = df.unique_pkt_lengths(ps)

    return int(page_id), feature_dict

def mean_packet_length(aggregate_features):
    fig, axs = plt.subplots(1, 2)
    axs[0].bar([feature[0] for feature in aggregate_features['mean_length_in']],[feature[1] for feature in aggregate_features['mean_length_in']])
    axs[0].set_xlabel("Repository")
    axs[0].set_ylabel("Mean Packet Length (Inbound)")

    axs[1].bar([feature[0] for feature in aggregate_features['mean_length_out']],[feature[1] for feature in aggregate_features['mean_length_out']],color='orange')
    axs[1].tick_params(axis='y')
    axs[1].yaxis.tick_right()
    axs[1].yaxis.set_label_position('right')
    axs[1].set_xlabel("Repository")
    axs[1].set_ylabel("Mean Packet Length (Outbound)")
    fig.set_size_inches(8, 3)
    plt.tight_layout()
    plt.savefig("mean-packet-length.png",dpi=300)

def mean_interarrival_time(aggregate_features):
    fig, axs = plt.subplots(1, 2)
    axs[0].bar([feature[0] for feature in aggregate_features['inter_mean_in']],[feature[1] for feature in aggregate_features['inter_mean_in']])
    axs[0].set_xlabel("Repository")
    axs[0].set_ylabel("Mean Interarrival Time (Inbound)")

    axs[1].bar([feature[0] for feature in aggregate_features['inter_mean_out']],[feature[1] for feature in aggregate_features['inter_mean_out']],color='orange')
    axs[1].tick_params(axis='y')
    axs[1].yaxis.tick_right()
    axs[1].yaxis.set_label_position('right')
    axs[1].set_xlabel("Repository")
    axs[1].set_ylabel("Mean Interarrival Time (Outbound)")
    fig.set_size_inches(8, 3)
    plt.tight_layout()
    plt.savefig("interarrival-times.png",dpi=300)

def unique_packet_lengths(aggregate_features):    
    fig, axs = plt.subplots(1, 2)
    axs[0].bar([feature[0] for feature in aggregate_features['unique_len_in']],[feature[1] for feature in aggregate_features['unique_len_in']])
    axs[0].set_xlabel("Repository")
    axs[0].set_ylabel("Unique Packet Lengths (Inbound)")

    axs[1].bar([feature[0] for feature in aggregate_features['unique_len_out']],[feature[1] for feature in aggregate_features['unique_len_out']],color='orange')
    axs[1].tick_params(axis='y')
    axs[1].yaxis.tick_right()
    axs[1].yaxis.set_label_position('right')
    axs[1].set_xlabel("Repository")
    axs[1].set_ylabel("Unique Packet Lengths (Outbound)")
    fig.set_size_inches(8, 3)
    plt.tight_layout()
    plt.savefig("unique-packet-lengths.png",dpi=300)

def extract_features(data_dir):
    file_list = [f for f in os.listdir(data_dir) if f.find('-') != -1]
    # file_list = file_list[:5]
    print(f'Found {len(file_list)} raw data files.')
    
    print('Extracting features.')
    aggregate_by_load = {}
    for file in tqdm(file_list):
        repo_id, feature_dict = file_to_features(os.path.join(data_dir,file))

        if repo_id in aggregate_by_load:
            aggregate_by_load[repo_id].append(feature_dict)
        else:
            aggregate_by_load[repo_id] = [feature_dict]
    
    aggregate_features = {}
    for repo_id in aggregate_by_load:
        repo_features = aggregate_by_load[repo_id]
        repo_aggregate = {}
        for key in repo_features[0]:
            feature_mean = np.mean([load[key] for load in repo_features])
            feature_mean = (repo_id, feature_mean)
            if key in aggregate_features:
                aggregate_features[key].append(feature_mean)
            else:
                aggregate_features[key] = [feature_mean]
    
    for key in aggregate_features:
        aggregate_features[key] = sorted(aggregate_features[key], key=lambda x: x[0])
    
    mean_packet_length(aggregate_features)
    mean_interarrival_time(aggregate_features)
    unique_packet_lengths(aggregate_features)
    



def main():
    data_dir = '../process/pdata/'
    extract_features(data_dir)

if __name__ == "__main__":
    main()