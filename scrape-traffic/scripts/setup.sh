docker build -t tcpdump $1
docker run -d -v file:/file tcpdump
# docker run -it -v file:/file tcpdump bash
# find . -type f | cut -d/ -f2 | sort | uniq -c
