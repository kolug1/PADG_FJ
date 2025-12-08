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

        self.view.button_add_class.config(command=lambda: self.add_class())
        self.view.button_delete_class.config(command=lambda: self.delete_class())
        self.view.button_edit_class.config(command=lambda: self.edit_class())

        self.view.button_add_student.config(command=lambda: self.add_student())
        self.view.button_delete_student.config(command=lambda: self.delete_student())
        self.view.button_edit_student.config(command=lambda: self.edit_student())

        self.view.combobox_school_for_student.bind("<<ComboboxSelected>>", self.update_class_combobox)

        self.school_info()
        self.employee_info()
        self.class_info()
        self.student_info()


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
        self.class_info()
        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)
        self.draw_markers()
        self.student_info()

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

        classes_to_keep = []
        for class_ in self.classes_data:
            if class_.school_name != school_name_to_delete:
                classes_to_keep.append(class_)

        self.classes_data = classes_to_keep
        self.class_info()
        self.draw_markers()
        self.employee_info()
        self.class_info()
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

        for class_ in self.classes_data:
            if class_.school_name == old_school_name:
                class_.school_name = school.name

        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)

        self.school_info()
        self.employee_info()
        self.class_info()
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

############KLASY############

    def class_info(self):
        self.view.listbox_classes.delete(0, END)

        for idx, class_ in enumerate(self.classes_data):
            self.view.listbox_classes.insert(idx, f"{class_.name} {class_.school_name}")

        school_names = [school.name for school in self.schools_data]
        self.view.combobox_school_for_class['values'] = school_names

    def add_class(self) -> None:
        name: str = self.view.entry_class_name.get()
        school_name: str = self.view.combobox_school_for_class.get()
        class_ = Class(name=name, school_name=school_name)
        self.classes_data.append(class_)
        self.class_info()
        self.view.entry_class_name.delete(0, END)
        self.view.combobox_school_for_class.set('')


    def delete_class(self):
        i = self.view.listbox_classes.index(ACTIVE)
        class_to_delete = self.classes_data[i]
        class_name_to_delete = class_to_delete.name
        school_name_to_delete = class_to_delete.school_name

        self.classes_data.pop(i)
        self.class_info()

        students_to_keep = []
        for student in self.students_data:
            if not (student.class_name == class_name_to_delete and student.school_name == school_name_to_delete):
                students_to_keep.append(student)
            else:
                self.markers[student].delete()
        self.students_data = students_to_keep
        self.student_info()

    def edit_class(self):
        i = self.view.listbox_classes.index(ACTIVE)
        class_ = self.classes_data[i]
        self.view.entry_class_name.delete(0, END)
        self.view.entry_class_name.insert(0, class_.name)
        self.view.combobox_school_for_class.set(class_.school_name)
        self.view.button_add_class.config(
            text="Zapisz zmiany",
            command=lambda: self.update_class(i)
        )

    def update_class(self, i):
        class_ = self.classes_data[i]
        class_.name = self.view.entry_class_name.get()
        class_.school_name = self.view.combobox_school_for_class.get()

        self.view.entry_class_name.delete(0, END)
        self.view.combobox_school_for_class.set('')

        self.class_info()
        self.view.button_add_class.config(
            text="Dodaj Klasę",
            command=lambda: self.add_class()
        )

############KLASY############

############UCZNIOWIE############

    def student_info(self):
        self.view.listbox_students.delete(0, END)

        for idx, student in enumerate(self.students_data):
            self.view.listbox_students.insert(idx, f"{student.name} {student.school_name} {student.class_name}")

        school_names = [school.name for school in self.schools_data]
        self.view.combobox_school_for_student['values'] = school_names

    def add_student(self) -> None:
        name: str = self.view.entry_student_name.get()
        address: str = self.view.entry_student_address.get()
        school_name: str = self.view.combobox_school_for_student.get()
        class_name: str = self.view.combobox_class_for_student.get()
        student = Student(name=name, school_name=school_name, class_name=class_name, position=None, location=address)
        self.students_data.append(student)
        self.student_info()
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.combobox_school_for_student.set('')
        self.view.combobox_class_for_student.set('')
        self.draw_markers()

    def delete_student(self):
        i = self.view.listbox_students.index(ACTIVE)
        student_to_delete = self.students_data[i]
        self.markers[student_to_delete].delete()
        self.students_data.pop(i)
        self.student_info()

    def edit_student(self):
        if not self.students_data:
            return
        i = self.view.listbox_students.index(ACTIVE)
        student = self.students_data[i]
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.entry_student_name.insert(0, student.name)
        self.view.entry_student_address.insert(0, student.location)
        self.view.combobox_school_for_student.set(student.school_name)
        self.update_class_combobox(None)
        self.view.combobox_class_for_student.set(student.class_name)
        self.view.button_add_student.config(
            text="Zapisz zmiany",
            command=lambda: self.update_student(i)
        )

    def update_student(self, i):
        student = self.students_data[i]
        student.name = self.view.entry_student_name.get()
        student.location = self.view.entry_student_address.get()
        student.school_name = self.view.combobox_school_for_student.get()
        student.class_name = self.view.combobox_class_for_student.get()
        student.coords = get_coordinates(student.location)

        marker = self.markers[student]
        marker.set_position(student.coords[0], student.coords[1])
        marker.set_text(student.name)

        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.combobox_school_for_student.set('')
        self.view.combobox_class_for_student.set('')

        self.student_info()
        self.view.button_add_student.config(
            text="Dodaj Ucznia",
            command=lambda: self.add_student()
        )

    def update_class_combobox(self, event):
        school_name = self.view.combobox_school_for_student.get()
        class_names = [class_.name for class_ in self.classes_data if class_.school_name == school_name]
        self.view.combobox_class_for_student['values'] = class_names

############UCZNIOWIE############
