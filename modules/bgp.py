'''
Python Version: 2.7
Nanog 72 Hackathon
'''

from napalm import get_network_driver


class Napalm_hack():
    def __init__(self, arg):
        self.arg = arg

    def get_remote_interface_mtu(driver_type, interface_name, device_name):
        """
        This function returns the mtu on the local interface and remote interface
        input - driver_type == Junos or eos, interface_name= outgoing interface, device_name=ip or hostname of the device
        output - {'remote_interface_mtu': 1500, 'local_interface_mtu': 1500}
        """
        result = {}
        result['remote_interface_mtu'] = 0
        result['local_interface_mtu'] = 0
        if driver_type == "junos":
            result['remote_interface_mtu'] = 1514
            result['local_interface_mtu'] = 1514
            return result
        try:
            driver = get_network_driver(driver_type)
            device = driver(device_name, 'ntc', 'ntc123')
            device.open()
            data = device.get_lldp_neighbors_detail(interface=interface_name)
            interface_lldp_details = dict(data).get(interface_name)
            cmd = "show interfaces {} | grep MTU".format(interface_name)
            temp = device.cli(commands=[cmd, ])
            device.close()
            for d in temp.keys():
                result['local_interface_mtu'] = int(temp[d].strip().split()[2])
            remote_port = interface_lldp_details[0].get('remote_port').replace('"','')
            remote_system_name = interface_lldp_details[0].get('remote_system_name').replace('.ntc.com','')
            if remote_system_name.startswith('eos'):
                remote_driver_type = 'eos'
            elif "vmx" in remote_system_name:
                remote_driver_type = 'junos'
            remote_driver = get_network_driver(remote_driver_type)
            remote_driver = remote_driver(remote_system_name, 'ntc', 'ntc123')
            remote_driver.open()
            if remote_driver_type == "eos":
                cmd = "show interfaces {} | grep MTU".format(remote_port)
                temp = remote_driver.cli(commands=[cmd,])
                for d in temp.keys():
                    result['remote_interface_mtu'] = int(temp[d].strip().split()[2])
            elif remote_driver_type == "junos":
                result['remote_interface_mtu'] = 1514
            remote_driver.close()
        except Exception as e:
            return result
        return result


    def outgoing_interface(out_data,routerid,segment_device_type,segment_name):

    	k=re.compile(r'{0}.*'.format(routerid))
    	finalkey=filter(k.match,out_data.keys())
    	try:
    		interface_p=out_data[finalkey[0]]
    		interface1=interface_p[0]
    		interface=interface1['outgoing_interface']
    	except:
    		finalkey=out_data.keys()
    		interface_p=out_data[finalkey[0]]
    		interface1=interface_p[0]
                    interface=interface1['outgoing_interface']
    	final = get_remote_interface_mtu(segment_device_type, interface_name=interface, device_name=segment_name)
    	final["interface"]=interface
    	final["segment_name"]=segment_name
    	if final["local_interface_mtu"] != final['remote_interface_mtu']:
    		mismatch="MTU interface Mismatch"
    	else:
    		mismatch= "SWEET!!"
    	final['Mismatch Details']=mismatch
    	return final

    def flatten(details):
    	shorten={}
    	inner={}
    	listinner=[]
    	for  k in details.keys():
    		for as_detail in details[k]:
    			shorten[k]={}
    			for vals in details[k][as_detail]:
    				#pprint(vals)
    				inner={}
    				inner['configured_holdtime']=vals['configured_holdtime']
    				inner['configured_keepalive']=vals['configured_keepalive']
    				inner['connection_state']=vals['connection_state']
    				inner['flap_count']=vals['flap_count']
                                    inner['holdtime']=vals['holdtime']
                                    inner['last_event']=vals['last_event']
    				inner['local_address']=vals['local_address']
                                    inner['local_as']=vals['local_as']
                                    inner['remote_address']=vals['remote_address']
                                    inner['remote_as']=vals['remote_as']
                                    inner['router_id']=vals['router_id']
                                    inner['up']=vals['up']
    				listinner.append(inner)
    		shorten[k][as_detail]=listinner
    	return shorten,listinner

        def compare_ram(ram):
            '''
            This Function checks if the RAM is exceeding >> 70 percent of the total ram.
            Required Parameters:
                ram - this is the output of device.get_environment() in the napalm library. (Type: Dict)
            '''
            compare_mem=ram['memory']
            totalmem=compare_mem['available_ram']+compare_mem['used_ram']
            if compare_mem['available_ram'] <= 0.7*totalmem:
                    field = "All okay"
            else:
                    field= "Ram Exceeding"
