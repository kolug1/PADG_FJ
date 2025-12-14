from tkinter import *
import tkinter.ttk as ttk
import tkintermapview
from padg_lib.model import schools

class MapView:
    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("1025x760")
        self.root.title("System zarządzania szkołami")

        self.ramka_zarzadania = Frame(root)
        self.ramka_mapa = Frame(root)

        self.ramka_zarzadania.grid(row=0, column=0, sticky=N)
        self.ramka_mapa.grid(row=1, column=0)

        self.create_menage_frame(self.ramka_zarzadania)
        self.create_map_frame()

        self.hide_dynamic_frames()
        self.show_frame("Szkoły")

    def create_menage_frame(self, parent):


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

        self.selected_category = StringVar()
        categories = ["Szkoły", "Klasy", "Pracownicy", "Uczniowie"]

        self.combobox_kategoria = ttk.Combobox(
            category_frame,
            textvariable=self.selected_category,
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

        Label(frame, text="LISTA KLAS").grid(row=0, column=0, sticky=W)
        self.listbox_classes = Listbox(frame)
        self.listbox_classes.grid(row=1, column=0)

        self.button_delete_class = Button(frame, text="Usuń Klasę")
        self.button_delete_class.grid(row=5, column=0, sticky=W)

        self.button_edit_class = Button(frame, text="Edytuj Klasę")
        self.button_edit_class.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Klasy").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Nazwa:").grid(row=1, column=0, sticky=W)
        self.entry_class_name = Entry(formularz)
        self.entry_class_name.grid(row=1, column=1)

        self.selected_school_for_class = StringVar()
        Label(formularz, text="Szkoła:").grid(row=2, column=0, sticky=W)
        self.combobox_school_for_class = ttk.Combobox(
            formularz,
            textvariable=self.selected_school_for_class,
            values=[],
            state="readonly"
        )
        self.combobox_school_for_class.grid(row=2, column=1)

        self.button_add_class = Button(formularz, text="Dodaj Klasę")
        self.button_add_class.grid(row=3, column=0, columnspan=2)
        return frame

    def create_employee_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="LISTA PRACOWNIKÓW").grid(row=0, column=0, sticky=W)
        #TODO zrobić dla pracowników
        self.listbox_employees = Listbox(frame)
        self.listbox_employees.grid(row=1, column=0)

        self.button_delete_employee = Button(frame, text="Usuń Pracownika")
        self.button_delete_employee.grid(row=5, column=0, sticky=W)

        self.button_edit_employee = Button(frame, text="Edytuj Pracownika")
        self.button_edit_employee.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Pracownika").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Imię:").grid(row=1, column=0, sticky=W)
        self.entry_employee_name = Entry(formularz)
        self.entry_employee_name.grid(row=1, column=1)

        Label(formularz, text="Miasto:").grid(row=2, column=0, sticky=W)
        self.entry_employee_city = Entry(formularz)
        self.entry_employee_city.grid(row=2, column=1)

        Label(formularz, text="Adres:").grid(row=3, column=0, sticky=W)
        self.entry_employee_street = Entry(formularz)
        self.entry_employee_street.grid(row=3, column=1)

        Label(formularz, text="Stanowisko:").grid(row=4, column=0, sticky=W)
        self.entry_employee_position = Entry(formularz)
        self.entry_employee_position.grid(row=4, column=1)

        self.selected_school = StringVar()
        Label(formularz, text="Szkoła:").grid(row=5, column=0, sticky=W)
        self.entry_employee_school = ttk.Combobox(
            formularz,
            textvariable=self.selected_school,
            values=[],
            state="readonly"
        )
        self.entry_employee_school.grid(row=5, column=1)

        self.button_add_employee = Button(formularz, text="Dodaj Pracownika")
        self.button_add_employee.grid(row=6, column=0, columnspan=2)
        return frame

    def create_student_frame(self, parent):
        frame = Frame(parent)
        Label(frame, text="LISTA UCZNIÓW").grid(row=0, column=0, sticky=W)
        self.listbox_students = Listbox(frame)
        self.listbox_students.grid(row=1, column=0)

        self.button_delete_student = Button(frame, text="Usuń Ucznia")
        self.button_delete_student.grid(row=5, column=0, sticky=W)

        self.button_edit_student = Button(frame, text="Edytuj Ucznia")
        self.button_edit_student.grid(row=5, column=1, sticky=W)

        formularz = Frame(frame)
        formularz.grid(row=1, column=1, sticky=N)
        Label(formularz, text="Formularz Ucznia").grid(row=0, column=0, columnspan=2)

        Label(formularz, text="Imię:").grid(row=1, column=0, sticky=W)
        self.entry_student_name = Entry(formularz)
        self.entry_student_name.grid(row=1, column=1)

        Label(formularz, text="Adres:").grid(row=2, column=0, sticky=W)
        self.entry_student_address = Entry(formularz)
        self.entry_student_address.grid(row=2, column=1)

        self.selected_school_for_student = StringVar()
        Label(formularz, text="Szkoła:").grid(row=3, column=0, sticky=W)
        self.combobox_school_for_student = ttk.Combobox(
            formularz,
            textvariable=self.selected_school_for_student,
            values=[],
            state="readonly"
        )
        self.combobox_school_for_student.grid(row=3, column=1)

        self.selected_class_for_student = StringVar()
        Label(formularz, text="Klasa:").grid(row=4, column=0, sticky=W)
        self.combobox_class_for_student = ttk.Combobox(
            formularz,
            textvariable=self.selected_class_for_student,
            values=[],
            state="readonly"
        )
        self.combobox_class_for_student.grid(row=4, column=1)

        self.button_add_student = Button(formularz, text="Dodaj Ucznia")
        self.button_add_student.grid(row=5, column=0, columnspan=2)
        return frame


    def hide_dynamic_frames(self):
        for frame in [self.school_frame, self.class_frame, self.employee_frame, self.student_frame]:
            frame.grid_forget()

    def show_frame(self, frame_name):
        self.hide_dynamic_frames()
        if frame_name == "Szkoły":
            self.school_frame.grid(row=0, column=0)
        elif frame_name == "Klasy":
            self.class_frame.grid(row=0, column=0)
        elif frame_name == "Pracownicy":
            self.employee_frame.grid(row=0, column=0)
        elif frame_name == "Uczniowie":
            self.student_frame.grid(row=0, column=0)


    def create_map_frame(self):
        # RAMKA MAPY
        self.map_widget = tkintermapview.TkinterMapView(self.ramka_mapa, width=1025, height=600)
        self.map_widget.set_position(52.19, 21.01)
        self.map_widget.set_zoom(11)
        self.map_widget.grid(row=0, column=0)