import sys, pprint

# helper function
def data_get(data, path, default = None):
    keys = path.split('.')
    try:
        for key in keys:
            # 加入對列表的處理
            if key.isdigit():
                data = data[int(key)]
            else:
                data = data[key]
        return data
    except (KeyError, TypeError, IndexError):
        return default

def dd(*args):
    for arg in args:
        pprint.pprint(arg, None, 1, 120)
    sys.exit()

def dump(*args):
    for arg in args:
        pprint.pprint(arg, None, 1, 120)