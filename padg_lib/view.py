from tkinter import *
import tkinter.ttk as ttk
import tkintermapview

class MapView:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1025x760")
        self.root.title("System zarządzania szkołami")

        self.ramka_zarzadania = Frame(root)
        self.ramka_mapa = Frame(root)

        self.ramka_zarzadania.grid(row=0, column=0, sticky=N)
        self.ramka_mapa.grid(row=1, column=0)

        self.create_zarzadzanie_frame(self.ramka_zarzadania)
        self.create_map_frame()

        self.hide_dynamic_frames()
        self.show_frame("Szkoły")

    def create_zarzadzanie_frame(self, parent):


        self.create_combobox(parent)

        self.dynamic_frame_container = Frame(parent)
        self.dynamic_frame_container.grid(row=1, column=0, columnspan=1, sticky='nsew')

        self.school_frame = self.create_school_frame(self.dynamic_frame_container)
        self.class_frame = self.create_class_frame(self.dynamic_frame_container)
        self.employee_frame = self.create_employee_frame(self.dynamic_frame_container)
        self.student_frame = self.create_student_frame(self.dynamic_frame_container)


    def create_combobox(self, parent):

        category_frame = Frame(parent)
        category_frame.grid(row=0, column=0, sticky=W)

        Label(category_frame, text="Wybierz kategorię:").grid(row=0, column=0, sticky=W)

        self.kategoria_do_pracy = StringVar()
        categories = ["Szkoły", "Klasy", "Pracownicy", "Uczniowie"]

        self.combobox_kategoria = ttk.Combobox(
            category_frame,
            textvariable=self.kategoria_do_pracy,
            values=categories,
            state="readonly"
        )
        self.combobox_kategoria.set(categories[0])
        self.combobox_kategoria.grid(row=0, column=1)



    def create_school_frame(self, parent):
        frame = Frame(parent)

        Label(frame, text="LISTA SZKÓŁ").grid(row=0, column=0, sticky=W)
        self.listbox_schools = Listbox(frame)
        self.listbox_schools.grid(row=1, column=0)

        self.button_delete_school = Button(frame, text="Usuń Szkołę")
        self.button_delete_school.grid(row=5, column=0, sticky=W)

        self.button_edit_school = Button(frame, text="Edytuj Szkołe")
        self.button_edit_school.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Szkoły").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Nazwa:").grid(row=1, column=0, sticky=W)
        self.entry_school_name = Entry(formularz)
        self.entry_school_name.grid(row=1, column=1)

        Label(formularz, text="Miasto:").grid(row=2, column=0, sticky=W)
        self.entry_school_city = Entry(formularz)
        self.entry_school_city.grid(row=2, column=1)

        Label(formularz, text="Adres:").grid(row=3, column=0, sticky=W)
        self.entry_school_street = Entry(formularz)
        self.entry_school_street.grid(row=3, column=1)

        self.button_add_school = Button(formularz, text="Dodaj Szkołę")
        self.button_add_school.grid(row=4, column=0, columnspan=2)

        return frame

    def create_class_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="ZARZĄDZANIE KLASAMI").grid(row=0, column=0, sticky=W)
        #
        return frame

    def create_employee_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="ZARZĄDZANIE PRACOWNIKAMI").grid(row=0, column=0, sticky=W)
        #
        return frame

    def create_student_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="ZARZĄDZANIE UCZNIAMI").grid(row=0, column=0, sticky=W)
        #
        return frame


    def hide_dynamic_frames(self):
        for frame in [self.school_frame, self.class_frame, self.employee_frame, self.student_frame]:
            frame.pack_forget()

    def show_frame(self, frame_name):
        self.hide_dynamic_frames()
        if frame_name == "Szkoły":
            self.school_frame.pack(fill='both', expand=True)
        elif frame_name == "Klasy":
            self.class_frame.pack(fill='both', expand=True)
        elif frame_name == "Pracownicy":
            self.employee_frame.pack(fill='both', expand=True)
        elif frame_name == "Uczniowie":
            self.student_frame.pack(fill='both', expand=True)


    def create_map_frame(self):
        # RAMKA MAPY
        self.map_widget = tkintermapview.TkinterMapView(self.ramka_mapa, width=1025, height=600)
        self.map_widget.set_position(52.0, 21.0)
        self.map_widget.set_zoom(10)
        self.map_widget.grid(row=0, column=0)