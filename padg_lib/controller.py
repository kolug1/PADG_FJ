from tkinter import *
from padg_lib.view import MapView
from padg_lib.model import School, Class, Employee, Student, schools, classes, employees, students, get_coordinates
import tkintermapview


class MapController:
    def __init__(self, root: Tk, view: MapView):
        self.root = root
        self.view = view

        self.view.combobox_kategoria.bind("<<ComboboxSelected>>", self.category_selection)

        self.schools_data:list = schools
        self.employees_data:list = employees
        self.students_data:list = students
        self.classes_data:list = classes

        self.markers: dict = {}

        self.view.button_add_school.config(command=lambda: self.add_school())
        self.view.button_delete_school.config(command=lambda: self.delete_school())
        self.view.button_edit_school.config(command=lambda: self.edit_school())

        self.view.button_add_employee.config(command=lambda: self.add_employee())
        self.view.button_delete_employee.config(command=lambda: self.delete_employee())
        self.view.button_edit_employee.config(command=lambda: self.edit_employee())


    def category_selection(self, event):
        selected_category = self.view.selected_category.get()
        self.view.show_frame(selected_category)


    def draw_markers(self):
        for obj, marker_instance in self.markers.items():
            marker_instance.delete()
        self.markers = {}
        objects_to_draw = self.schools_data + self.employees_data + self.students_data
        for obj in objects_to_draw:
                marker = self.view.map_widget.set_marker(obj.coords[0], obj.coords[1], text=obj.name)
                self.markers[obj] = marker


############SZKOŁY############

    def school_info(self):
        self.view.listbox_schools.delete(0, END)

        for idx, school in enumerate(self.schools_data):
            self.view.listbox_schools.insert(idx, f"{school.name} {school.city} {school.street}")

        school_names = [school.name for school in self.schools_data]
        self.view.entry_employee_school['values'] = school_names

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

    def delete_school(self):
        i = self.view.listbox_schools.index(ACTIVE)
        school_to_delete = self.schools_data[i]
        school_name_to_delete = school_to_delete.name

        self.markers[school_to_delete].delete()
        self.schools_data.pop(i)
        self.school_info()

        employees_to_keep = []
        for employee in self.employees_data:
            if employee.school_name != school_name_to_delete:
                employees_to_keep.append(employee)
            else:
                self.markers[employee].delete()

        self.employees_data = employees_to_keep
        self.draw_markers()
        self.employee_info()
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
            if not self.schools_data:
                return
            i = self.view.listbox_schools.index(ACTIVE)
            school = self.schools_data[i]
            self.view.entry_school_name.delete(0, END)
            self.view.entry_school_city.delete(0, END)
            self.view.entry_school_street.delete(0, END)
            self.view.entry_school_name.insert(0, school.name)
            self.view.entry_school_city.insert(0, school.city)
            self.view.entry_school_street.insert(0, school.street)
            self.view.button_add_school.config(
                text="Zapisz zmiany",
                command=lambda: self.update_school(i)
            )
    #
    #
    def update_school(self, i):
        school = self.schools_data[i]
        old_school_name = school.name

        school.name = self.view.entry_school_name.get()
        school.city = self.view.entry_school_city.get()
        school.street = self.view.entry_school_street.get()
        address = f"{school.city}, {school.street}"
        school.coords = get_coordinates(address)

        marker = self.markers[school]
        marker.set_position(school.coords[0], school.coords[1])
        marker.set_text(school.name)

        for employee in self.employees_data:
            if employee.school_name == old_school_name:
                employee.school_name = school.name

        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)

        self.school_info()
        self.employee_info()
        self.view.button_add_school.config(
            text="Dodaj obiekt",
            command=lambda: self.add_school()
        )

############SZKOŁY############

############PRACOWNICY############

    def employee_info(self):
        self.view.listbox_employees.delete(0, END)

        for idx, employee in enumerate(self.employees_data):
            self.view.listbox_employees.insert(idx, f"{employee.name} {employee.city} {employee.street}")

    def add_employee(self) -> None:
        name: str = self.view.entry_employee_name.get()
        city: str = self.view.entry_employee_city.get()
        street: str = self.view.entry_employee_street.get()
        school_name: str = self.view.entry_employee_school.get()
        position: str = self.view.entry_employee_position.get()
        employee = Employee(name=name, city=city, street=street, school_name=school_name, position=position)
        self.employees_data.append(employee)
        self.employee_info()
        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)
        self.view.entry_employee_position.delete(0, END)
        self.draw_markers()

    def delete_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee_delete = self.employees_data[i]
        self.markers[employee_delete].delete()
        self.employees_data.pop(i)
        self.employee_info()

    def edit_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee = self.employees_data[i]
        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)
        self.view.entry_employee_position.delete(0, END)
        self.view.entry_employee_name.insert(0, employee.name)
        self.view.entry_employee_city.insert(0, employee.city)
        self.view.entry_employee_street.insert(0, employee.street)
        self.view.entry_employee_school.set(employee.school_name)
        self.view.entry_employee_position.insert(0, employee.position)
        self.view.button_add_employee.config(
            text="Zapisz zmiany",
            command=lambda: self.update_employee(i)
        )

    def update_employee(self, i):
        employee = self.employees_data[i]

        employee.name = self.view.entry_employee_name.get()
        employee.city = self.view.entry_employee_city.get()
        employee.street = self.view.entry_employee_street.get()
        employee.school_name = self.view.entry_employee_school.get()
        employee.position = self.view.entry_employee_position.get()
        address = f"{employee.city}, {employee.street}"
        employee.coords = get_coordinates(address)

        marker = self.markers[employee]
        marker.set_position(employee.coords[0], employee.coords[1])
        marker.set_text(employee.name)

        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)
        self.view.entry_employee_position.delete(0, END)

        self.employee_info()
        self.view.button_add_employee.config(
            text="Dodaj Pracownika",
            command=lambda: self.add_employee()
        )



############PRACOWNICY############
