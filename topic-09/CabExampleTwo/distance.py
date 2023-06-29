from geopy.distance import geodesic


def calculatedistance(long1: float, lat1: float, long2: float, lat2: float) -> float:
    """
    Calculates the distance between two points on the earth's surface
    :rtype: float
    :param long1:
    :param lat1:
    :param long2:
    :param lat2:
    :return: distance between two points in km
    """
    customer = (lat1, long1)
    taxi = (lat2, long2)
    distance = geodesic(customer, taxi).km
    return distance
