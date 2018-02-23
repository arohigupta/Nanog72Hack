'''
Python Version: 2.7
Author: arohi.gupta@colorado.edu
Nanog 72 Hackathon
'''

import re
from bgp import Napalm_hack
from pprint import PrettyPrinter
from pprint import pprint
from napalm import get_network_driver
from prettytable import PrettyTable
from operator import itemgetter
from formatting import Formatter
import yaml
import time


if __name__ == '__main__':
	with open("/config_files/devices.yaml", 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
        dict1=cfg['devices']
	for segment in dict1:
		driver = get_network_driver(segment['device_type'])
		segment_device_type=segment['device_type']
		segment_name=segment['name']
        	with driver(segment['name'], 'ntc', 'ntc123') as device:
        		details=device.get_bgp_neighbors_detail()
            	ram=device.get_environment()
                field=Napalm_hack.compare_ram(ram)
            	shorten,innerlist=Napalm_hack.flatten(details)
			routerids=[]
			for ele in innerlist:
				if ele['router_id']:
					routerids.append(ele['router_id'])
                	RAMdetails={}
                	RAMdetails['Available_Ram']=compare_mem['available_ram']
                	RAMdetails['Status']=field
                	t = PrettyTable(['Available Ram', 'Field'])
                	for key, val in RAMdetails.items():
                        	t.add_row([key, val])
                	keys=['configured_holdtime','configured_keepalive','connection_state','flap_count','holdtime','last_event','local_address','local_as','remote_address','remote_as','router_id','up']
                	print Formatter.format_as_table(innerlist,keys,keys)
			print "*"*20
			print "CONFIG TESTS"
			print "*"*20
			print t
			mtu_final=[]
			for ele in routerids:
                		out_data=device.get_route_to(ele)
                		mtu_fi=Napalm_hack.outgoing_interface(out_data,ele,segment_device_type,segment_name)
				mtu_final.append(mtu_fi)
			print "*"*20
			print "Mismatch Details"
			print "*"*20
			keys=['interface','local_interface_mtu','remote_interface_mtu','segment_name','Mismatch Details']
			print format_as_table(mtu_final,keys,keys)
			print "*"*20
