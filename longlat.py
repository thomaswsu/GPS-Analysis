from geopy import distance, Point
from math import sin, cos, sqrt, atan2, radians

def convert(tude: str) -> float:
    """ Convert weird latidute and longitde strings to decimal representation
    """
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return(multiplier * float(tude[:-1]))

def convert_long_and_lat_to_distance(lat1: float, long1: float, lat2: float, long2: float) -> float:

    lat1 = convert(lat1)
    long1 = convert(long1)
    lat2 = convert(lat2)
    long2 = convert(long2)

    point1 = (lat1, long1)
    point2 = (lat2, long2)
    return(distance.distance(point1, point2).m)


def convert_long_and_lat_list_to_distance_list(lattitude: list, longitute: list) -> list:
    """ This function takes in a series of lattitude and longitute list of strings and returns the change
    in distance as a list. In other words, this function calculates the change in distance between
    longitute and lattitude points and returns the change in distance a list of floats. 
    """
    ret = [0] # first row has no previous refererance so its 0 
    for i in range(1, len(lattitude)):
        ret.append(convert_long_and_lat_to_distance(lattitude[i -1], longitute[i -1], \
            lattitude[i], longitute[i]))
    return(ret)

""" Sources:
https://stackoverflow.com/questions/21298772/how-to-convert-latitude-longitude-to-decimal-in-python
https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
"""