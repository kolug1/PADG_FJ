
import tkintermapview

users: list = []

class User:
    def __init__(self, name: str, location: str, posts: int, img_url: str, map_widget: tkintermapview.TkinterMapView):
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        url:str=f'https://nominatim.openstreetmap.org/search?q={self.location}&format=json&limit=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        data=requests.get(url, headers=headers).json()
        latitude=float(data[0]['lat'])
        longitude=float(data[0]['lon'])
        return [latitude, longitude]

