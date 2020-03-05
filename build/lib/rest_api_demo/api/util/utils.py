def csv_to_list(csv):
    """
    Convert csv to python list
    """
    if type(csv) is str or type(csv) is unicode: 
        csv = ''.join(csv.split())
        return csv.split(',')
    elif type(csv) is list:
        return csv