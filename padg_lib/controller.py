from tkinter import *
from padg_lib.view import MapView
from padg_lib.model import School, Class, Employee, Student, schools, classes, employees, students, get_coordinates


class MapController:
    def __init__(self, root: Tk, view: MapView):
        self.root = root
        self.view = view

        self.view.combobox_kategoria.bind("<<ComboboxSelected>>", self.category_selection)

        self.schools_data:list = schools
        self.displayed_schools:list = list(schools)
        self.employees_data:list = employees
        self.displayed_employees:list = list(employees)
        self.students_data:list = students
        self.displayed_students:list = list(students)
        self.classes_data:list = classes

        self.markers: dict = {}

        self.view.button_add_school.config(command=lambda: self.add_school())
        self.view.button_delete_school.config(command=lambda: self.delete_school())
        self.view.button_edit_school.config(command=lambda: self.edit_school())
        self.view.button_show_on_map.config(command=self.show_schools_on_map)
        self.view.button_reset_school_filter.config(command=self.reset_school_filters)

        self.view.button_add_employee.config(command=lambda: self.add_employee())
        self.view.button_delete_employee.config(command=lambda: self.delete_employee())
        self.view.button_edit_employee.config(command=lambda: self.edit_employee())
        self.view.button_filter_employees.config(command=self.filter_employees)
        self.view.button_reset_employee_filter.config(command=self.reset_employee_filters)

        self.view.button_add_class.config(command=lambda: self.add_class())
        self.view.button_delete_class.config(command=lambda: self.delete_class())
        self.view.button_edit_class.config(command=lambda: self.edit_class())

        self.view.button_add_student.config(command=lambda: self.add_student())
        self.view.button_delete_student.config(command=lambda: self.delete_student())
        self.view.button_edit_student.config(command=lambda: self.edit_student())
        self.view.button_filter_students.config(command=self.filter_students)
        self.view.button_reset_student_filter.config(command=self.reset_student_filters)

        self.view.combobox_school_for_student.bind("<<ComboboxSelected>>", self.update_class_combobox)
        self.view.entry_student_filter_school.bind("<<ComboboxSelected>>", self.update_student_filter_class_combobox)

        self.school_info()
        self.employee_info()
        self.class_info()
        self.student_info()


    def category_selection(self, event):
        selected_category = self.view.selected_category.get()
        self.view.show_frame(selected_category)
        if selected_category == "Szkoły":
            self.show_schools_on_map()
        elif selected_category == "Pracownicy":
            self.filter_employees()
        elif selected_category == "Uczniowie":
            self.filter_students()
        else:
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}


    def show_schools_on_map(self):
        city_filter = self.view.entry_map_city_filter.get()

        self.view.listbox_schools.delete(0, END)

        if city_filter:
            self.displayed_schools = [school for school in self.schools_data if school.city.lower() == city_filter.lower()]
        else:
            self.displayed_schools = list(self.schools_data)

        if self.view.selected_category.get() == "Szkoły":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}
            
            for idx, school in enumerate(self.displayed_schools):
                if hasattr(school, 'coords') and school.coords:
                    marker = self.view.map_widget.set_marker(school.coords[0], school.coords[1], text=school.name)
                    self.markers[school] = marker
                self.view.listbox_schools.insert(idx, f"{school.name} {school.city} {school.street}")
        else:
            for idx, school in enumerate(self.displayed_schools):
                self.view.listbox_schools.insert(idx, f"{school.name} {school.city} {school.street}")



    def reset_school_filters(self):
        self.view.entry_map_city_filter.delete(0, END)
        self.show_schools_on_map()

    def reset_employee_filters(self):
        self.view.entry_employee_filter_city.delete(0, END)
        self.view.entry_employee_filter_school.set('')
        self.filter_employees()

    def reset_student_filters(self):
        self.view.entry_student_filter_school.set('')
        self.view.entry_student_filter_class.set('')
        self.filter_students()


############SZKOŁY############

    def school_info(self):
        self.show_schools_on_map()

        school_names = [school.name for school in self.schools_data]
        self.view.entry_employee_school['values'] = school_names
        self.view.entry_employee_filter_school['values'] = school_names

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
        self.student_info()

    def delete_school(self):
        i = self.view.listbox_schools.index(ACTIVE)
        school_to_delete = self.displayed_schools[i]

        school_name_to_delete = school_to_delete.name

        if school_to_delete in self.markers:
            self.markers[school_to_delete].delete()
        
        if school_to_delete in self.schools_data:
            self.schools_data.remove(school_to_delete)
        
        self.school_info()

        employees_to_keep = []
        for employee in self.employees_data:
            if employee.school_name != school_name_to_delete:
                employees_to_keep.append(employee)
            else:
                if employee in self.markers:
                    self.markers[employee].delete()

        self.employees_data = employees_to_keep

        classes_to_keep = []
        for class_ in self.classes_data:
            if class_.school_name != school_name_to_delete:
                classes_to_keep.append(class_)

        self.classes_data = classes_to_keep
        self.class_info()
        self.employee_info()
        self.class_info()
        self.student_info()
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
            school = self.displayed_schools[i]

            self.view.entry_school_name.delete(0, END)
            self.view.entry_school_city.delete(0, END)
            self.view.entry_school_street.delete(0, END)
            self.view.entry_school_name.insert(0, school.name)
            self.view.entry_school_city.insert(0, school.city)
            self.view.entry_school_street.insert(0, school.street)
            self.view.button_add_school.config(
                text="Zapisz zmiany",
                command=lambda: self.update_school(school)
            )
    #
    #
    def update_school(self, school):
        old_school_name = school.name

        school.name = self.view.entry_school_name.get()
        school.city = self.view.entry_school_city.get()
        school.street = self.view.entry_school_street.get()
        address = f"{school.city}, {school.street}"
        school.coords = get_coordinates(address)

        if school in self.markers:
            marker = self.markers[school]
            marker.set_position(school.coords[0], school.coords[1])
            marker.set_text(school.name)

        for employee in self.employees_data:
            if employee.school_name == old_school_name:
                employee.school_name = school.name

        for class_ in self.classes_data:
            if class_.school_name == old_school_name:
                class_.school_name = school.name

        for student in self.students_data:
            if student.school_name == old_school_name:
                student.school_name = school.name

        self.view.entry_school_name.delete(0, END)
        self.view.entry_school_city.delete(0, END)
        self.view.entry_school_street.delete(0, END)

        self.school_info()
        self.employee_info()
        self.class_info()
        self.student_info()
        self.view.button_add_school.config(
            text="Dodaj obiekt",
            command=lambda: self.add_school()
        )

############SZKOŁY############

############PRACOWNICY############

    def filter_employees(self):
        city_filter = self.view.entry_employee_filter_city.get()
        school_filter = self.view.entry_employee_filter_school.get()

        self.view.listbox_employees.delete(0, END)

        filtered = self.employees_data
        if city_filter:
            filtered = [e for e in filtered if e.city.lower() == city_filter.lower()]
        if school_filter:
            filtered = [e for e in filtered if e.school_name == school_filter]
        
        self.displayed_employees = list(filtered)

        if self.view.selected_category.get() == "Pracownicy":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}

            for idx, employee in enumerate(self.displayed_employees):
                if hasattr(employee, 'coords') and employee.coords:
                    marker = self.view.map_widget.set_marker(employee.coords[0], employee.coords[1], text=employee.name)
                    self.markers[employee] = marker
                self.view.listbox_employees.insert(idx, f"{employee.name} {employee.city} {employee.street}")
        else:
             for idx, employee in enumerate(self.displayed_employees):
                self.view.listbox_employees.insert(idx, f"{employee.name} {employee.city} {employee.street}")

    def employee_info(self):
        self.filter_employees()

    def add_employee(self) -> None:
        name: str = self.view.entry_employee_name.get()
        city: str = self.view.entry_employee_city.get()
        street: str = self.view.entry_employee_street.get()
        school_name: str = self.view.entry_employee_school.get()
        employee = Employee(name=name, city=city, street=street, school_name=school_name)
        self.employees_data.append(employee)
        self.employee_info()
        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)

    def delete_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee_delete = self.displayed_employees[i]

        if employee_delete in self.markers:
            self.markers[employee_delete].delete()
        
        if employee_delete in self.employees_data:
            self.employees_data.remove(employee_delete)
        
        self.employee_info()

    def edit_employee(self):
        i = self.view.listbox_employees.index(ACTIVE)
        employee = self.displayed_employees[i]

        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)
        self.view.entry_employee_name.insert(0, employee.name)
        self.view.entry_employee_city.insert(0, employee.city)
        self.view.entry_employee_street.insert(0, employee.street)
        self.view.entry_employee_school.set(employee.school_name)
        self.view.button_add_employee.config(
            text="Zapisz zmiany",
            command=lambda: self.update_employee(employee)
        )

    def update_employee(self, employee):
        
        employee.name = self.view.entry_employee_name.get()
        employee.city = self.view.entry_employee_city.get()
        employee.street = self.view.entry_employee_street.get()
        employee.school_name = self.view.entry_employee_school.get()
        address = f"{employee.city}, {employee.street}"
        employee.coords = get_coordinates(address)

        if employee in self.markers:
            marker = self.markers[employee]
            marker.set_position(employee.coords[0], employee.coords[1])
            marker.set_text(employee.name)

        self.view.entry_employee_name.delete(0, END)
        self.view.entry_employee_city.delete(0, END)
        self.view.entry_employee_street.delete(0, END)
        self.view.entry_employee_school.delete(0, END)
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
        self.student_info()


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
        old_name = class_.name
        old_school = class_.school_name

        class_.name = self.view.entry_class_name.get()
        class_.school_name = self.view.combobox_school_for_class.get()

        for student in self.students_data:
            if student.class_name == old_name and student.school_name == old_school:
                student.class_name = class_.name
                student.school_name = class_.school_name

        self.view.entry_class_name.delete(0, END)
        self.view.combobox_school_for_class.set('')

        self.class_info()
        self.view.button_add_class.config(
            text="Dodaj Klasę",
            command=lambda: self.add_class()
        )

############KLASY############

############UCZNIOWIE############

    def filter_students(self):
        school_filter = self.view.entry_student_filter_school.get()
        class_filter = self.view.entry_student_filter_class.get()

        self.view.listbox_students.delete(0, END)

        filtered = self.students_data
        if school_filter:
            filtered = [s for s in filtered if s.school_name == school_filter]
        if class_filter:
            filtered = [s for s in filtered if s.class_name == class_filter]
        
        self.displayed_students = list(filtered)

        if self.view.selected_category.get() == "Uczniowie":
            for obj, marker_instance in self.markers.items():
                marker_instance.delete()
            self.markers = {}

            for idx, student in enumerate(self.displayed_students):
                if hasattr(student, 'coords') and student.coords:
                    marker = self.view.map_widget.set_marker(student.coords[0], student.coords[1], text=student.name)
                    self.markers[student] = marker
                self.view.listbox_students.insert(idx, f"{student.name} {student.school_name} {student.class_name}")
        else:
            for idx, student in enumerate(self.displayed_students):
                self.view.listbox_students.insert(idx, f"{student.name} {student.school_name} {student.class_name}")

    def student_info(self):
        self.filter_students()
        
        school_names = [school.name for school in self.schools_data]
        self.view.combobox_school_for_student['values'] = school_names
        self.view.entry_student_filter_school['values'] = school_names

    def add_student(self) -> None:
        name: str = self.view.entry_student_name.get()
        address: str = self.view.entry_student_address.get()
        school_name: str = self.view.combobox_school_for_student.get()
        class_name: str = self.view.combobox_class_for_student.get()
        student = Student(name=name, school_name=school_name, class_name=class_name, location=address, position='')
        self.students_data.append(student)
        self.student_info()
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.combobox_school_for_student.set('')
        self.view.combobox_class_for_student.set('')

    def delete_student(self):
        i = self.view.listbox_students.index(ACTIVE)
        student_to_delete = self.displayed_students[i]

        if student_to_delete in self.markers:
            self.markers[student_to_delete].delete()
        
        if student_to_delete in self.students_data:
            self.students_data.remove(student_to_delete)
        
        self.student_info()

    def edit_student(self):
        i = self.view.listbox_students.index(ACTIVE)
        student = self.displayed_students[i]
        
        self.view.entry_student_name.delete(0, END)
        self.view.entry_student_address.delete(0, END)
        self.view.entry_student_name.insert(0, student.name)
        self.view.entry_student_address.insert(0, student.location)
        self.view.combobox_school_for_student.set(student.school_name)
        self.update_class_combobox(None)
        self.view.combobox_class_for_student.set(student.class_name)
        self.view.button_add_student.config(
            text="Zapisz zmiany",
            command=lambda: self.update_student(student)
        )

    def update_student(self, student):
        
        student.name = self.view.entry_student_name.get()
        student.location = self.view.entry_student_address.get()
        student.school_name = self.view.combobox_school_for_student.get()
        student.class_name = self.view.combobox_class_for_student.get()
        student.coords = get_coordinates(student.location)

        if student in self.markers:
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
    
    def update_student_filter_class_combobox(self, event):
        school_name = self.view.entry_student_filter_school.get()
        class_names = [class_.name for class_ in self.classes_data if class_.school_name == school_name]
        self.view.entry_student_filter_class['values'] = class_names

############UCZNIOWIE############
