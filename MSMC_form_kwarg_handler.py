'''
Due to Flask form input for Msmc_clustering instances being read as strings,
helper functions are needed to convert certain arguments to their correct
data types.
'''


def manual_modify_dict(my_dict: "dict",
                       to_int_list: "list[int]",
                       to_float_list: "list[float]",
                       to_bool_list: "list[bool]",
                       to_list_list: "list[list]") -> "dict":
    my_dict = to_int(to_int_list, my_dict)
    my_dict = to_float(to_float_list, my_dict)
    my_dict = to_bool(to_bool_list, my_dict)
    my_dict = to_li(to_list_list, my_dict)
    return my_dict


def to_int(to_int_list: "list[str]",
           my_dict: "dict") -> "dict":
    '''
    Converts values in my_dict to ints based on the kwargs from to_int_list.
    '''
    for thing in to_int_list:
        my_dict[thing] = int(my_dict[thing])
    return my_dict


def to_float(to_float_list: "list[str]",
             my_dict: "dict") -> "dict":
    '''
    Converts values in my_dict to floats based on the kwargs from
    to_float_list.
    '''
    for thing in to_float_list:
        my_dict[thing] = float(my_dict[thing])
    return my_dict


def to_bool(to_bool_list: "list[str]",
            my_dict: "dict") -> "dict":
    '''
    Converts values in my_dict to bools based on the kwargs from to_bool_list.
    '''
    for thing in to_bool_list:
        my_dict[thing] = my_dict[thing] == 'True'
    return my_dict


def to_li(to_list_list: "list[str]",
          my_dict: "dict") -> "dict":
    '''
    Converts values in my_dict to lists based on the kwargs from to_list_list.
    '''
    for thing in to_list_list:
        umm = thing.split(',')
        if len(umm) > 1:
            my_dict[thing] = [float(t) for t in umm]
            print(my_dict[thing])
    return my_dict
