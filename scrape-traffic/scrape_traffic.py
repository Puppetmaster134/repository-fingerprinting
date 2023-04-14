import os,json,uuid,subprocess,atexit,psutil,shutil
from dotenv import dotenv_values
from process_trace import load_packet_data

def create_directories(env):
    #Create the directory to store packet data
    if not os.path.isdir(env['DATA']):
        os.mkdir(env['DATA'])
    if not os.path.isdir(f"{env['DATA']}/{env['run_id']}"):
        os.mkdir(f"{env['DATA']}/{env['run_id']}")
    
    #Create the directory to dump downloaded files
    if not os.path.isdir(env['FILES']):
        os.mkdir(env['FILES'])
    else:
        delete_old_downloads(env['FILES'])
    
# some function i found online that will kill all children spawned by tcpdump
def kill_process_and_children(pid: int, sig: int = 15):
    try:
        proc = psutil.Process(pid)
    except psutil.NoSuchProcess as e:
        # Maybe log something here
        return

    for child_process in proc.children(recursive=True):
        child_process.send_signal(sig)

    proc.send_signal(sig)

def delete_old_downloads(filedump):
    #Get a list of all files in the directory
    dl_files = [f"{filedump}/{f}" for f in os.listdir(filedump) if os.path.isfile(f)]
    for file in dl_files:
        os.remove(file)

#function to start tcpdump
def start_tcpdump(device, packet_file):
    command = f"tcpdump -n -i {device} -w {packet_file}"
    run_cmd = subprocess.Popen(command,shell=True)

    kill_it = lambda : kill_process_and_children(run_cmd.pid)
    atexit.register(kill_it)
    return run_cmd

#function to start download
def start_download(url, filedump):
    command = f"wget {url} -O {filedump}/{url[url.rfind('/') + 1:]}"
    run_cmd = subprocess.run(command, shell=True)
    return run_cmd

def delete_file(location):
    os.remove(location)

def fetch_wget_files(env, resources):
    #Loop through each resource and scrape it
    for element in resources:
        #Where to save the data
        packet_file = f"{env['DATA']}/{env['run_id']}/{element['name']}"

        #Start tcpdump and return the process
        tcpdump = start_tcpdump(env['DEVICE'],packet_file)
        
        #Start a file download with wget and return the process
        url = element['url']
        wget = start_download(url, env['FILES'])

        #Kill tcpdump gracefully
        kill_process_and_children(tcpdump.pid)

        #Delete data
        # delete_old_downloads(env['FILES'])
        delete_file(f"{env['FILES']}/{url[url.rfind('/') + 1:]}")

#function to clone git repos
def start_clone_repo(url, filedump):
    command = f"git clone {url} {filedump}/{url[url.rfind('/') + 1:]}"
    run_cmd = subprocess.run(command, shell=True)
    return run_cmd

#deletes a repo when we're done with it
def delete_repo(location):
    try:
        shutil.rmtree(location)
    except FileNotFoundError:
        print(f"Couldn't delete repo at {location}")

def save_trace(filename, processed_trace):
    with open(filename, 'w') as f:
        for size, time in processed_trace:
            f.write(f"{size}\t{time}\n")

def fetch_git_repos(env, resources):
    for element in resources:
        #Where to save the data
        filename = f"{env['DATA']}/{env['run_id']}/{element['name']}"

        #Start tcpdump and return the process
        tcpdump = start_tcpdump(env['DEVICE'], f"{filename}.pcap")

        #Fetch the git repo
        url = element['url']
        git = start_clone_repo(url, env['FILES'])

        #Kill tcpdump gracefully
        kill_process_and_children(tcpdump.pid)

        #Delete downloaded repo
        delete_repo(f"{env['FILES']}/{url[url.rfind('/') + 1:]}")

        try:
            #Process trace
            processed_trace = load_packet_data(f"{filename}.pcap")

            #Save trace_data
            save_trace(filename, processed_trace)
        except:
            print(f"Failed to process trace for {element['name']}")

        #Delete pcap
        os.remove(f"{filename}.pcap")


def run_scrape():
    env = dotenv_values() if os.path.exists(".env") else dotenv_values("image.env")
    
    #Set RunID
    env['run_id'] = uuid.uuid4()
    print(env['run_id'])

    #Load in the settings containing which resources to download
    with open('./data-settings.json') as f:
        data_settings = json.load(f)

    #Ensure the directory structure is fine
    create_directories(env)

    #Download wget files
    # fetch_wget_files(env, data_settings['wget-files'])

    #Download git repos
    fetch_git_repos(env, data_settings['git-repos'])

    #todo: vs code plugins via cli

def main():
    n_scrapes = 50

    for i in range(n_scrapes):
        run_scrape()


      

if __name__ == "__main__":
    main()