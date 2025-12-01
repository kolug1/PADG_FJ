from tkinter import *
import tkintermapview

class MapView:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1025x760")
        self.root.title("System zarządzania szkołami")

        self.ramka_lista_obiektow = Frame(root)
        self.ramka_formularz = Frame(root)
        self.ramka_szczegolow_obiektu = Frame(root)
        self.ramka_mapa = Frame(root)

        self.ramka_lista_obiektow.grid(row=0, column=0)
        self.ramka_formularz.grid(row=0, column=1)
        self.ramka_szczegolow_obiektu.grid(row=1, column=0, columnspan=2)
        self.ramka_mapa.grid(row=2, column=0, columnspan=2)

        self.create_lista_obiektow_frame()
        self.create_formularz_frame()
        self.create_szczegoly_obiektu_frame()
        self.create_map_frame()

    def create_lista_obiektow_frame(self):
        Label(self.ramka_lista_obiektow, text="Lista obiektów").grid(row=0, column=0, columnspan=3)

        self.listbox_lista_obiektow = Listbox(self.ramka_lista_obiektow, width=35)
        self.listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

        self.button_pokaz_szczegoly = Button(self.ramka_lista_obiektow, text="Pokaż szczegóły")
        self.button_pokaz_szczegoly.grid(row=2, column=0)

        self.button_usun_obiekt = Button(self.ramka_lista_obiektow, text="Usuń obiekt")
        self.button_usun_obiekt.grid(row=2, column=1)

        self.button_edytuj_obiekt = Button(self.ramka_lista_obiektow, text="Edytuj obiekt")
        self.button_edytuj_obiekt.grid(row=2, column=2)

    def create_formularz_frame(self):
        Label(self.ramka_formularz, text="Formularz").grid(row=0, column=0, columnspan=2)

        Label(self.ramka_formularz, text="Imię").grid(row=1, column=0, sticky=W)
        Label(self.ramka_formularz, text="Lokalizacja").grid(row=2, column=0, sticky=W)
        Label(self.ramka_formularz, text="Liczba postów").grid(row=3, column=0, sticky=W)
        Label(self.ramka_formularz, text="Obrazek").grid(row=4, column=0, sticky=W)

        self.entry_name = Entry(self.ramka_formularz)
        self.entry_name.grid(row=1, column=1, sticky=W)

        self.entry_lokalizacja = Entry(self.ramka_formularz)
        self.entry_lokalizacja.grid(row=2, column=1)

        self.entry_posty = Entry(self.ramka_formularz)
        self.entry_posty.grid(row=3, column=1)

        self.entry_imgurl = Entry(self.ramka_formularz)
        self.entry_imgurl.grid(row=4, column=1)

        self.button_dodaj_obiekt = Button(self.ramka_formularz, text="Dodaj obiekt")
        self.button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

    def create_szczegoly_obiektu_frame(self):
        Label(self.ramka_szczegolow_obiektu, text="Szczegóły obiektu").grid(row=0, column=0, sticky=W, columnspan=6)

        Label(self.ramka_szczegolow_obiektu, text="Imię: ").grid(row=1, column=0)
        self.label_imie_szczegoly_obiektu_wartosc = Label(self.ramka_szczegolow_obiektu, text="....")
        self.label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)

        Label(self.ramka_szczegolow_obiektu, text="Lokalizacja: ").grid(row=1, column=2)
        self.label_lokalizacja_szczegoly_obiektu_wartosc = Label(self.ramka_szczegolow_obiektu, text="....")
        self.label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=3)

        Label(self.ramka_szczegolow_obiektu, text="Posty: ").grid(row=1, column=4)
        self.label_posty_szczegoly_obiektu_wartosc = Label(self.ramka_szczegolow_obiektu, text="....")
        self.label_posty_szczegoly_obiektu_wartosc.grid(row=1, column=5)

    def create_map_frame(self):
        # RAMKA MAPY
        self.map_widget = tkintermapview.TkinterMapView(self.ramka_mapa, width=1025, height=600)
        self.map_widget.set_position(52.0, 21.0)
        self.map_widget.set_zoom(10)
        self.map_widget.grid(row=0, column=0)