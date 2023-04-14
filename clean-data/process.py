import os, shutil

data_dir = './data'
out_dir = './pdata'
file_ids = {}
count = {}

def add_file_id(filename):
    id_max = 0 if not file_ids else max(file_ids.values()) + 1
    if filename not in file_ids:
        file_ids[filename] = id_max
    
    if filename not in count:
        count[filename] = 1
    else:
        count[filename] += 1
    
    return id_max

for idx, run_id in enumerate(os.listdir(data_dir)):
    for filename in os.listdir(f'{data_dir}/{run_id}'):
        file_id = add_file_id(filename)

for idx, run_id in enumerate(os.listdir(data_dir)):
    for filename in os.listdir(f'{data_dir}/{run_id}'):
        if count[filename] < 45:
            continue

        f_path = os.path.join(data_dir,run_id,filename)
        o_path = os.path.join(out_dir,f"{file_ids[filename]}-{idx}")

        with open(f_path,'r') as old_file:
            lines = old_file.readlines()
            with open(o_path,'w') as new_file:
                for line in lines:
                    vals = line.strip().split('\t')
                    vals.reverse()
                    reversed_line = '\t'.join(vals) + "\n"
                    new_file.write(reversed_line)
        # shutil.copy(f_path, o_path)

with open(os.path.join(out_dir,'id_index'),'w') as f:
    for k,v in file_ids.items():
        f.write(f'{v}:{k}\n')