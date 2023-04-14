FROM ubuntu 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install git gcc tcpdump python3.10 python3-dev python3.10-venv python-is-python3 openssh-server -y
ADD ./ssh/repo-key /
RUN chmod 600 /repo-key
RUN mkdir ~/.ssh && touch ~/.ssh/known_hosts && ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN eval `ssh-agent -s` && ssh-add ./repo-key && git clone "git@github.com:Puppetmaster134/sturdy-eureka.git"
RUN python -m venv ./sturdy-eureka/env
RUN cd sturdy-eureka && source ./env/bin/activate && pip install -r ./requirements.txt
CMD cd sturdy-eureka && source ./env/bin/activate && python scrape_traffic.py