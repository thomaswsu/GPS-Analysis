def convert_utc_to_decimal(utc_time: int, utc_offset: int) -> float:
    """ This formula doesn't seem to work...
    I'll do some more research on this 
    """
    return((utc_time + utc_offset * 3600) / 86400)

def convert_utc_list_to_decimal_list(utc_list: list, utc_offset) -> list:
    """ Takes in the a list of utc times and performs a conversion to decimal time on
    every item in the list.
    """
    ret = []
    for item in utc_list:
        ret.append(convert_utc_to_decimal(item, utc_offset))
    return(ret)