from github import Github
base_list = [
    {"name":"tor","url":"https://github.com/torproject/tor"},
    {"name":"stegotorus","url":"https://github.com/SRI-CSL/stegotorus"},
    {"name":"castle","url":"https://github.com/bridgar/Castle-Covert-Channel"},
    {"name":"scramblesuit","url":"https://github.com/NullHypothesis/scramblesuit"},
    {"name":"skypemorph","url":"https://github.com/blizzardplus/Code-Talker-Tunnel"},
    {"name":"deltashaper","url":"https://github.com/dmbb/DeltaShaper"},
    {"name":"protozoa","url":"https://github.com/dmbb/Protozoa"},
    {"name":"telex","url":"https://github.com/ewust/telex"},
    {"name":"slitheen","url":"https://github.com/zhums/slitheen"},
    {"name":"meek","url":"https://github.com/arlolra/meek"},
    {"name":"shadowsocks","url":"https://github.com/shadowsocks/shadowsocks-windows"},
    {"name":"v2ray","url":"https://github.com/v2ray/v2ray-core"},
    {"name":"shadowtls","url":"https://github.com/ihciah/shadow-tls"}
]


key =  ""
g = Github(key)
n = 110
tc = g.search_repositories("stars:>1 -topic:roadmap -topic:lists -topic:books",sort="stars",order="desc")[:n - len(base_list)]
data = [*base_list, *[{"name":repo.name,"url":repo.clone_url} for repo in tc]]

import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)