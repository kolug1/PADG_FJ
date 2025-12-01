from tkinter import *
from padg_lib.view import MapView
from padg_lib.model import School
import tkintermapview


class MapController:
    def __init__(self, root: Tk, view: MapView):
        self.root = root
        self.view = view
        self.users_data: list = []

        self.view.button_dodaj_obiekt.config(command=lambda: self.add_user())
        self.view.button_usun_obiekt.config(command=lambda: self.delete_user())
        self.view.button_pokaz_szczegoly.config(command=lambda: self.user_details())
        self.view.button_edytuj_obiekt.config(command=lambda: self.edit_user())

        self.user_info()

    def user_info(self):
        self.view.listbox_lista_obiektow.delete(0, END)

        for idx, user in enumerate(self.users_data):
            self.view.listbox_lista_obiektow.insert(idx, f"{user.name} {user.location} {user.posts}")

    def add_user(self) -> None:

        name: str = self.view.entry_name.get()
        location: str = self.view.entry_lokalizacja.get()
        posts: int = int(self.view.entry_posty.get())
        img_url: str = self.view.entry_imgurl.get()

        user = User(name=name, location=location, posts=posts, img_url=img_url,
                              map_widget=self.view.map_widget)
        self.users_data.append(user)

        print(self.users_data)  # Zgodnie z oryginalną funkcją

        # 3. Aktualizacja widoku Listbox
        self.user_info()

        # 4. Czyszczenie pól i ustawienie focusa
        self.view.entry_name.delete(0, END)
        self.view.entry_lokalizacja.delete(0, END)
        self.view.entry_posty.delete(0, END)
        self.view.entry_imgurl.delete(0, END)
        self.view.entry_name.focus()


    def delete_user(self):
        i = self.view.listbox_lista_obiektow.curselection()[0]
        self.users_data[i].marker.delete()
        self.users_data.pop(i)
        self.user_info()


    def user_details(self):
            # Pobierz indeks aktywnego elementu
            i = self.view.listbox_lista_obiektow.curselection()[0]
            user = self.users_data[i]

            # 1. Uaktualnij szczegóły w widoku (View)
            self.view.label_imie_szczegoly_obiektu_wartosc.config(text=user.name)
            self.view.label_lokalizacja_szczegoly_obiektu_wartosc.config(text=user.location)
            self.view.label_posty_szczegoly_obiektu_wartosc.config(text=user.posts)

            # 2. Ustaw pozycję i zoom mapy
            self.view.map_widget.set_position(user.coords[0], user.coords[1])
            self.view.map_widget.set_zoom(14)


    def edit_user(self):
            # Pobierz indeks aktywnego elementu
            i = self.view.listbox_lista_obiektow.curselection()[0]
            user = self.users_data[i]

            # 1. Czyszczenie i wstawianie danych do pól formularza
            self.view.entry_name.delete(0, END)
            self.view.entry_lokalizacja.delete(0, END)
            self.view.entry_posty.delete(0, END)
            self.view.entry_imgurl.delete(0, END)

            self.view.entry_name.insert(0, user.name)
            self.view.entry_lokalizacja.insert(0, user.location)
            self.view.entry_posty.insert(0, user.posts)
            self.view.entry_imgurl.insert(0, user.img_url)

            # 2. Zmiana przycisku na "Zapisz zmiany" z komendą update_user(i)
            self.view.button_dodaj_obiekt.config(
                text="Zapisz zmiany",
                command=lambda: self.update_user(i)
            )


    def update_user(self, i):
        user = self.users_data[i]

        # 1. Aktualizacja danych obiektu (z widoku)
        user.name = self.view.entry_name.get()
        user.location = self.view.entry_lokalizacja.get()
        user.posts = int(self.view.entry_posty.get())
        user.img_url = self.view.entry_imgurl.get()

        user.coords = user.get_coordinates()
        user.marker.set_position(user.coords[0], user.coords[1])
        user.marker.set_text(user.name)

        self.view.entry_lokalizacja.delete(0, END)
        self.view.entry_posty.delete(0, END)
        self.view.entry_imgurl.delete(0, END)
        self.view.button_dodaj_obiekt.config(
            text="Dodaj obiekt",
            command=lambda: self.add_user()
        )

        self.user_info()

