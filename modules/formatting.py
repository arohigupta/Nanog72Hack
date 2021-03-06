'''
Python Version: 2.7
Author: arohi.gupta@colorado.edu
Nanog 72 Hackathon
'''

class Formatter():
    def format_as_table(data,
                        keys,
                        header=None,self):

    """Takes a list of dictionaries, formats the data, and returns
    the formatted data as a text table.

    Required Parameters:
        data - Data to process (list of dictionaries). (Type: List)
        keys - List of keys in the dictionary. (Type: List)

    Optional Parameters:
        header - The table header. (Type: List)
        sort_by_key - The key to sort by. (Type: String)
        sort_order_reverse - Default sort order is ascending, if
            True sort order will change to descending. (Type: Boolean)
    """

        sort_by_key=None
        sort_order_reverse=False
        if sort_by_key:
            data = sorted(data,
                          key=itemgetter(sort_by_key),
                          reverse=sort_order_reverse)
        if header:
            header_divider = []
            for name in header:
                header_divider.append('-' * len(name))
            header_divider = dict(zip(keys, header_divider))
            data.insert(0, header_divider)
            header = dict(zip(keys, header))
            data.insert(0, header)
        column_widths = []
        for key in keys:
            column_widths.append(max(len(str(column[key])) for column in data))
        key_width_pair = zip(keys, column_widths)

        format = ('%-*s ' * len(keys)).strip() + '\n'
        formatted_data = ''
        for element in data:
            data_to_format = []
            # Create a tuple that will be used for the formatting in
            # width, value format
            for pair in key_width_pair:
                data_to_format.append(pair[1])
                data_to_format.append(element[pair[0]])
            formatted_data += format % tuple(data_to_format)
        return formatted_data

    def pretty(shorten,self):
            """Takes a dictionary, formats the data, and returns
            the formatted data as a pretty table.

            Required Parameters:
                shorten - Data to process (dictionary). (Type: Dict)
            """
    	t = PrettyTable(['key', 'value'])
    	for key, val in shorten.items():
    		t.add_row([key, val])
    	print t
