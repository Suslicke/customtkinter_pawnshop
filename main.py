import os
from tkinter import ttk, messagebox
import customtkinter
from customtkinter import CTkButton, CTkEntry, CTkLabel, CTkInputDialog, CTk, CTkFrame, CTkComboBox
from models import Users, Students, Roles
from db import loop


class LoginWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("180x340")
        self.resizable(False, False)

        self.title("Авторизация")
        
        self.surname_label = CTkLabel(self, text="Фамилия")
        self.surname_label.pack()
        self.surname = CTkEntry(self, placeholder_text="Иванов")
        self.surname.pack()
        
        
        self.first_name_label = CTkLabel(self, text="Имя")
        self.first_name_label.pack()
        self.first_name = CTkEntry(self, placeholder_text="Иван")
        self.first_name.pack()
        
        
        self.patronymic_label = CTkLabel(self, text="Отчество")
        self.patronymic_label.pack()
        self.patronymic = CTkEntry(self, placeholder_text="Иванович")
        self.patronymic.pack()


        self.patronymic_label = CTkLabel(self, text="Пароль")
        self.patronymic_label.pack()
        self.password_entry = CTkEntry(self, show="*")
        self.password_entry.pack()
        
        self.error_label = CTkLabel(self, text="Неверные данные")
        

        self.submit_button = CTkButton(
            master=self,
            text="Авторизоваться",
            command=self.check_credentials,
        )
        self.submit_button.pack(padx=20, pady=20)


    def check_credentials(self):
        first_name = self.first_name.get()
        surname = self.surname.get()
        patronymic = self.patronymic.get()
        
        password = self.password_entry.get()
        
        user = loop.run_until_complete(Users.filter(first_name=first_name, surname=surname, patronymic=patronymic).first())

        if user == None:
            self.error_label.pack()
        else:
            if user.password == password:
                self.destroy()
                
                app = Application(user)
                app.mainloop()
            else:
                self.error_label.pack()
                
                
class RegistrationWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("180x400")
        self.resizable(False, False)

        self.title("Регистрация")
        
        self.surname_label = CTkLabel(self, text="Фамилия")
        self.surname_label.pack()
        self.surname = CTkEntry(self, placeholder_text="Иванов")
        self.surname.pack()
        
        
        self.first_name_label = CTkLabel(self, text="Имя")
        self.first_name_label.pack()
        self.first_name = CTkEntry(self, placeholder_text="Иван")
        self.first_name.pack()
        
        
        self.patronymic_label = CTkLabel(self, text="Отчество")
        self.patronymic_label.pack()
        self.patronymic = CTkEntry(self, placeholder_text="Иванович")
        self.patronymic.pack()


        self.password_label = CTkLabel(self, text="Пароль")
        self.password_label.pack()
        self.password_entry = CTkEntry(self, show="*")
        self.password_entry.pack()
        
        self.role_label = CTkLabel(self, text="Роль")
        self.role_label.pack()
        self.role_entry = CTkComboBox(self, values=["Администратор", "Секретарь"])
        self.role_entry.pack()

                
        self.error_label = CTkLabel(self, text="Неверные данные")
        

        self.submit_button = CTkButton(
            master=self,
            text="Регистрация",
            command=self.registration,
        )
        self.submit_button.pack(padx=20, pady=20)

    def registration(self):
        
        self.roles = loop.run_until_complete(Roles.filter(name=self.role_entry.get()).first())
        
        loop.run_until_complete(Users.create(
            first_name=self.first_name.get(),
            surname=self.first_name.get(), 
            patronymic = self.patronymic.get(),
            password = self.password_entry.get(),
            access_level = self.roles
            ))
                    
        self.destroy()

        
class Application(CTk):
    def __init__(self, user=None):
        super().__init__()
        self.geometry("1410x295")
        self.resizable(False, False)

        self.user = user
        loop.run_until_complete(user.fetch_related('access_level'))
        self.title(f"Добро пожаловать, {self.user.first_name}!")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                        background="#333333",  
                        foreground="white", 
                        fieldbackground="#333333",
                        borderwidth=10, 
                        relief="solid"
                        ),

        style.map("Custom.Treeview",
                  background=[("selected", "#347083")])

        self.tree = ttk.Treeview(self, style="Custom.Treeview", columns=('ID', 'Surname', 'Name', 'Patronymic', 'Snils', 'Pasport', 'Address'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Surname', text='Фамилия')
        self.tree.heading('Name', text='Имя')
        self.tree.heading('Patronymic', text='Отчество')
        self.tree.heading('Snils', text='Снилс')
        self.tree.heading('Pasport', text='Паспорт')
        self.tree.heading('Address', text='Адрес')
        self.tree.grid(row=0)
        
        self.button_frame = CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=20, pady=20)
        self.update_button = CTkButton(self.button_frame, text="Обновить", command=self.update_table)
        self.create_button = CTkButton(self.button_frame, text="Добавить студента", command=self.create)
        self.delete_button = CTkButton(self.button_frame, text="Удалить", command=self.delete_selected)
        self.edit_button = CTkButton(self.button_frame, text="Изменить", command=self.edit_selected)
        self.export_button = CTkButton(self.button_frame, text="Экспорт", command=self.export)
        self.registration_button = CTkButton(self.button_frame, text="Регистрация", command=self.registration)
        
        self.logout_button = CTkButton(
            self.button_frame,
            text="Выйти",
            command=self.logout
        )
        
        self.update_button.pack(side="left", padx=5)
        self.export_button.pack(side="left", padx=5)
        self.edit_button.pack(side="left", padx=5)
        self.create_button.pack(side="left", padx=5)
        self.delete_button.pack(side="left", padx=5)

        self.update_table()
        
        if user.access_level != None:
            if user.access_level.name == "Администратор":
                self.registration_button.pack(side="left", padx=5)
                
        
        self.logout_button.pack(side="left", padx=5)
                
                
    def registration(self):
        app = RegistrationWindow()
        app.mainloop()


    def create(self):
        app = CreateDialog(on_finish=self.update_table)
        app.mainloop()
    
    
    def delete_selected(self):
        selected = self.tree.selection()
        if selected:    
            for select in selected:
                self.user_id = self.tree.item(select)['values'][0]
                self.user = loop.run_until_complete(Students.get(id=self.user_id))
                if self.user:
                    loop.run_until_complete(self.user.delete())
                    messagebox.showinfo("Info", "Данные были удалены")
                    self.update_table()
                else:
                    messagebox.showerror("Error", "Студент не найден")
        else:
            messagebox.showerror("Error", "Нет выбранного поля")
    
    
    def edit_selected(self):
        selected = self.tree.selection()
        if selected:    
            if len(selected) > 1:
                print("hellooo")
                try:
                    messagebox.showerror("Error", "Выбрано несколько полей, можно только 1")
                except:
                    pass
            else:    
                self.user_id = self.tree.item(selected)['values'][0]
                self.user = loop.run_until_complete(Students.get(id=self.user_id))
                app = EditDialog(user=self.user, on_finish=self.update_table)
                app.mainloop()
        else:
            messagebox.showerror("Error", "Нет выбранного поля")
        

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        students = loop.run_until_complete(Students.all())
        for student in students:
            self.tree.insert('', 'end', values=(student.id, student.surname, student.first_name, student.patronymic, student.snils, student.pasport, student.address))


    def export(self):
            selected = self.tree.selection()
            if selected:
                with open("ExportTXT.txt", "w", encoding="utf-8") as file:
                    for select in selected:
                        self.user_id = self.tree.item(select)['values'][0]
                        self.user = loop.run_until_complete(Students.get(id=self.user_id))
                        if self.user:
                            text = f"Имя: {self.user.first_name}\nФамилия: {self.user.surname}\nОтчество: {self.user.patronymic}\nСНИЛС: {self.user.snils}\nПаспорт: {self.user.pasport}\nАдрес: {self.user.address}\n\n"
                            file.write(text)
                        else:
                            messagebox.showerror("Error", "Студент не найден")
            else:
                messagebox.showerror("Error", "Нет выбранного поля")

            messagebox.showinfo("Info", "Данные были экспортированы в файл")
    
    def logout(self):
        self.destroy()        
        
        
class EditDialog(CTk):
    def __init__(self, user, on_finish=None):
        self.user = user
        self.on_finish = on_finish
        super().__init__()
        self.geometry("180x340")
        self.resizable(False, False)

        self.title("Редактирование пользователя")
        CTkLabel(self, text="Фамилия:").grid(row=0)
        CTkLabel(self, text="Имя:").grid(row=1)
        CTkLabel(self, text="Отчество:").grid(row=2)
        CTkLabel(self, text="СНИЛС:").grid(row=3)
        CTkLabel(self, text="Паспорт:").grid(row=4)
        CTkLabel(self, text="Адрес:").grid(row=5)


        self.name_entry = CTkEntry(self, placeholder_text="Иванов")
        self.name_entry.insert(0, self.user.first_name)
        self.name_entry.grid(row=0, column=1)
        
        self.surname_entry = CTkEntry(self, placeholder_text="Иван")
        self.surname_entry.insert(0, self.user.surname)
        self.surname_entry.grid(row=1, column=1)


        self.patronymic_entry = CTkEntry(self, placeholder_text="Иванович")
        self.patronymic_entry.insert(0, self.user.patronymic)
        self.patronymic_entry.grid(row=2, column=1)
        
        self.snils_entry = CTkEntry(self, placeholder_text="СНИЛС")
        self.snils_entry.insert(0, self.user.snils)
        self.snils_entry.grid(row=3, column=1)
        
        self.pasport_entry = CTkEntry(self, placeholder_text="Паспорт")
        self.pasport_entry.insert(0, self.user.pasport)
        self.pasport_entry.grid(row=4, column=1)
        
        self.address_entry = CTkEntry(self, placeholder_text="Адрес")
        self.address_entry.insert(0, self.user.address)
        self.address_entry.grid(row=5, column=1)
        
        self.apply_button = CTkButton(self, text="Сохранить", command=self.apply)
        self.apply_button.grid(row=6, column=1)


    def apply(self):
        
        self.user.first_name = self.name_entry.get()
        self.user.surname = self.surname_entry.get()
        self.user.patronymic = self.patronymic_entry.get()
        self.user.snils = self.snils_entry.get()
        self.user.pasport = self.pasport_entry.get()
        self.user.address = self.address_entry.get()
        
        loop.run_until_complete(self.user.save())
        if self.on_finish:
            self.on_finish()
            
        self.destroy()
        

class CreateDialog(CTk):
    def __init__(self, on_finish=None):
        self.on_finish = on_finish
        super().__init__()
        self.geometry("180x340")
        self.resizable(False, False)

        self.title("Редактирование пользователя")
        CTkLabel(self, text="Фамилия:").grid(row=0)
        CTkLabel(self, text="Имя:").grid(row=1)
        CTkLabel(self, text="Отчество:").grid(row=2)
        CTkLabel(self, text="СНИЛС:").grid(row=3)
        CTkLabel(self, text="Паспорт:").grid(row=4)
        CTkLabel(self, text="Адрес:").grid(row=5)


        self.name_entry = CTkEntry(self, placeholder_text="Иванов")
        self.name_entry.grid(row=0, column=1)
        
        self.surname_entry = CTkEntry(self, placeholder_text="Иван")
        self.surname_entry.grid(row=1, column=1)


        self.patronymic_entry = CTkEntry(self, placeholder_text="Иванович")
        self.patronymic_entry.grid(row=2, column=1)
        
        self.snils_entry = CTkEntry(self, placeholder_text="СНИЛС")
        self.snils_entry.grid(row=3, column=1)
        
        self.pasport_entry = CTkEntry(self, placeholder_text="Паспорт")
        self.pasport_entry.grid(row=4, column=1)
        
        self.address_entry = CTkEntry(self, placeholder_text="Адрес")
        self.address_entry.grid(row=5, column=1)
        
        self.apply_button = CTkButton(self, text="Сохранить", command=self.apply)
        self.apply_button.grid(row=6, column=1)


    def apply(self):
        
        loop.run_until_complete(Students.create(
            first_name=self.name_entry.get(),
            surname=self.surname_entry.get(), 
            patronymic = self.patronymic_entry.get(),
            snils = self.snils_entry.get(),
            pasport = self.pasport_entry.get(),
            address = self.address_entry.get())
                                )  

        if self.on_finish:
            self.on_finish()
            
        self.destroy()
        
        
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
    
