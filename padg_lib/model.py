
import tkintermapview

def _build_headers(self, provider_key, **kwargs):
    return {"User-Agent": 'My User Agent 1.0'}


def get_coordinates(address: str):
    from geocoder.osm import OsmQuery
    OsmQuery._build_headers = _build_headers
    data = tkintermapview.convert_address_to_coordinates(address)
    latitude = float(data[0])
    longitude = float(data[1])
    return [latitude, longitude]

schools: list = []
employees: list = []
students: list = []
classes: list = []

class School:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.coords = get_coordinates(address)


class Class:
    def __init__(self, name: str, school_name: str):
        self.name = name
        self.school_name = school_name

class Employee:
    def __init__(self, name: str, school_name: str, position: str, location: str):
        self.name = name
        self.school_name = school_name
        self.position = position
        self.location = location
        self.coords = get_coordinates(location)

class Student:
    def __init__(self, name: str, school_name: str, class_name: str, position: str, location: str):
        self.name = name
        self.school_name = school_name
        self.class_name = class_name
        self.location = location
        self.coords = get_coordinates(location)
