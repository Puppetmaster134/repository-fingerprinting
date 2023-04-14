import os,json,argparse,dpkt,datetime,socket
import pandas as pd
from dotenv import dotenv_values

def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def load_packet_data(filepath):
    # Open pcap in binary mode
    # ref: https://stackoverflow.com/questions/51968186/what-is-this-error-when-i-try-to-parse-a-simple-pcap-file
    with open(filepath,'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        packet_data = []
        
        for ts,buf in pcap:
            # Extract packet contents
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data

            # Dump what we want into a list
            packet_data.append({
                "src":inet_to_str(ip.src) if hasattr(ip,'src') else None, # Who sent it
                "dst":inet_to_str(ip.dst) if hasattr(ip,'dst') else None, # Who received it
                "ts":datetime.datetime.utcfromtimestamp(ts), # When
                # "size":len(tcp.data) if hasattr(tcp,'data') else () # How big was it
                "size":len(buf)
            })
        
        #Convert to dataframe
        df = pd.DataFrame.from_dict(packet_data)
        #Count packets from each source, drop packets from low count sources
        ips = [val for val in df['src'].value_counts().keys()][:2]
        likely_traffic = df.loc[df['src'].isin(ips)]

        base_ts = likely_traffic['ts'].iloc[0]
        local_ip = likely_traffic['src'].iloc[0]
        trace_data = []
        for index, row in likely_traffic.iterrows():
            seconds = (row['ts'] - base_ts).total_seconds()
            inbound = 1 if row['src'] == local_ip else -1
            trace_data.append((inbound * row['size'],seconds))

    return trace_data