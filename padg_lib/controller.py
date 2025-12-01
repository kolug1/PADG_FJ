from tkinter import *
from padg_lib.view import MapView
from padg_lib.model import School, Class, Employee, Student, schools, classes, employees, students, get_coordinates
import tkintermapview


class MapController:
    def __init__(self, root: Tk, view: MapView):
        self.root = root
        self.view = view

        self.schools_data:list = schools
        self.employees_data:list = employees
        self.students_data:list = students
        self.classes_data:list = classes

        self.markers: dict = {}

        self.view.button_add_school.config(command=lambda: self.add_school())
        self.view.button_delete_school.config(command=lambda: self.delete_school())
        self.view.button_edit_school.config(command=lambda: self.edit_school())

    def draw_markers(self):
        for obj, marker_instance in self.markers.items():
            marker_instance.delete()
        self.markers = {}
        objects_to_draw = self.schools_data + self.employees_data + self.students_data
        for obj in objects_to_draw:
                marker = self.view.map_widget.set_marker(obj.coords[0], obj.coords[1], text=obj.name)
                self.markers[obj] = marker


    def school_info(self):
        self.view.listbox_schools.delete(0, END)

        for idx, school in enumerate(self.schools_data):
            self.view.listbox_schools.insert(idx, f"{school.name} {school.city} {school.street}")

    def add_school(self) -> None:
        name: str = self.view.entry_school_name.get()
        city: str = self.view.entry_school_city.get()
        street: str = self.view.entry_school_street.get()
        school = School(name=name, city=city, street=street)
        self.schools_data.append(school)
        self.school_info()
        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)
        self.draw_markers()
        print (self.markers)

    def delete_school(self):
        i = self.view.listbox_schools.index(ACTIVE)
        self.markers[i].delete()
        self.schools_data.pop(i)
        self.school_info()
    #
    #
    # def user_details(self):
    #         i = self.view.listbox_lista_obiektow.curselection()[0]
    #         user = self.users_data[i]
    #
    #         self.view.label_imie_szczegoly_obiektu_wartosc.config(text=user.name)
    #         self.view.label_lokalizacja_szczegoly_obiektu_wartosc.config(text=user.location)
    #         self.view.label_posty_szczegoly_obiektu_wartosc.config(text=user.posts)
    #
    #         self.view.map_widget.set_position(user.coords[0], user.coords[1])
    #         self.view.map_widget.set_zoom(14)
    #
    #
    def edit_school(self):
            i = self.view.listbox_schools.curselection()[0]
            school = self.schools_data[i]
            self.view.entry_school_name.delete(0, END)
            self.view.entry_school_city.delete(0, END)
            self.view.entry_school_street.delete(0, END)
            self.view.entry_school_name.insert(0, school.name)
            self.view.entry_school_city.insert(0, school.city)
            self.view.entry_school_street.insert(0, school.street)
            self.view.button_add_school.config(
                text="Zapisz zmiany",
                command=lambda: self.update_user(i)
            )
    #
    #
    def update_user(self, i):
        school = self.schools_data[i]

        school.name = self.view.entry_school_name.get()
        school.city = self.view.entry_school_city.get()
        school.street = self.view.entry_school_street.get()
        school.coords = get_coordinates(f"{school.city}, {school.street}")

        marker = self.markers[school]
        marker.set_position(school.coords[0], school.coords[1])
        marker.set_text(school.name)


        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)

        self.school_info()
        self.view.button_add_school.config(
            text="Dodaj obiekt",
            command=lambda: self.add_school()
        )


