from shapely.geometry import Point
from shapely.geometry.polygon import Polygon




def tupleToPoint(t):
    return Point(t[0], t[1])

def collideRectPolygon(rect, polygon):
    # Creating the polygon
    polygon = Polygon(polygon)
    p0 = tupleToPoint(rect.topleft)
    if polygon.contains(p0):
        return True
    p1 = tupleToPoint(rect.topright)
    if polygon.contains(p1):
        return True
    p2 = tupleToPoint(rect.bottomleft)
    if polygon.contains(p2):
        return True
    p3 = tupleToPoint(rect.bottomright)
    if polygon.contains(p3):
        return True

    return False
