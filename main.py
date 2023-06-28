import os
from tkinter import ttk, messagebox
import customtkinter
from customtkinter import CTkButton, CTkEntry, CTkLabel, CTkInputDialog, CTk, CTkFrame, CTkComboBox
from models import Items, Users, Roles
from db import loop

def validate_float_input(input):
    try:
        if input:
            float(input)
        return True
    except ValueError:
        return False


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
        self.role_entry = CTkComboBox(self, values=["Администратор", "Оценщик"])
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
        self.geometry("1510x295")
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

        self.tree = ttk.Treeview(self, style="Custom.Treeview", columns=('ID', 'item_name', 'type_of_item', 'vescar', 'weight', 'price', 'first_name', 'surname', 'modified_at'), show='headings')
        
        column_widths = {'ID': 30, 'item_name': 200, 'type_of_item': 200, 'vescar': 100, 'weight': 100, 
                 'price': 100, 'first_name': 150, 'surname': 150, 'modified_at': 200}
        
        for column, width in column_widths.items():
            self.tree.column(column, width=width, stretch=False)

        self.tree.heading('ID', text='ID')
        self.tree.heading('item_name', text='Наименование товара')
        self.tree.heading('type_of_item', text='металл/драг. камень')
        self.tree.heading('vescar', text='Караты/Проба')
        self.tree.heading('weight', text='Масса')
        self.tree.heading('price', text='Цена')
        self.tree.heading('first_name', text='Имя')
        self.tree.heading('surname', text='Фамилия')
        self.tree.heading('modified_at', text='Дата')
        self.tree.grid(row=0)
        
        self.button_frame = CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=20, pady=20)
        self.update_button = CTkButton(self.button_frame, text="Обновить", command=self.update_table)
        self.create_button = CTkButton(self.button_frame, text="Добавить товар", command=self.create)
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
                self.item_id = self.tree.item(select)['values'][0]
                self.item = loop.run_until_complete(Items.get(id=self.item_id))
                if self.item:
                    loop.run_until_complete(self.item.delete())
                    messagebox.showinfo("Info", "Данные были удалены")
                    self.update_table()
                else:
                    messagebox.showerror("Error", "Товар не найден")
        else:
            messagebox.showerror("Error", "Нет выбранного поля")
    
    
    def edit_selected(self):
        selected = self.tree.selection()
        if selected:    
            if len(selected) > 1:
                try:
                    messagebox.showerror("Error", "Выбрано несколько полей, можно только 1")
                except:
                    pass
            else:    
                self.item_id = self.tree.item(selected)['values'][0]
                self.item = loop.run_until_complete(Items.get(id=self.item_id))
                app = EditDialog(item=self.item, on_finish=self.update_table)
                app.mainloop()
        else:
            messagebox.showerror("Error", "Нет выбранного поля")
        

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        items = loop.run_until_complete(Items.all())
        for item in items:
            self.tree.insert('', 'end', values=(item.id, item.item_name, item.type_of_item, item.vescar, item.weight, item.price, item.first_name, item.surname, item.modified_at))


    def export(self):
            selected = self.tree.selection()
            if selected:
                with open("ExportTXT.txt", "w", encoding="utf-8") as file:
                    for select in selected:
                        self.item_id = self.tree.item(select)['values'][0]
                        self.item = loop.run_until_complete(Items.get(id=self.item_id))
                        if self.user:
                            text = f"Наименование товара: {self.item.item_name}\nТип: {self.item.type_of_item}\nПроба/караты: {self.item.vescar}\nВес: {self.item.weight}\nЦена: {self.item.price}\nИмя: {self.item.first_name}\nФамилия: {self.item.surname}\nДата: {self.item.modified_at}\n\n"
                            file.write(text)
                        else:
                            messagebox.showerror("Error", "Товар не найден")
            else:
                messagebox.showerror("Error", "Нет выбранного поля")

            messagebox.showinfo("Info", "Данные были экспортированы в файл")
    
    def logout(self):
        self.destroy()        
        
        
class EditDialog(CTk):
    def __init__(self, item, on_finish=None):
        self.item = item
        self.on_finish = on_finish
        super().__init__()
        self.geometry("380x340")
        self.resizable(False, False)

        self.title("Редактирование пользователя")
        CTkLabel(self, text="Наименование товара:").grid(row=0)
        CTkLabel(self, text="металл/драг. камень: ").grid(row=1)
        CTkLabel(self, text="Караты/Проба:").grid(row=2)
        CTkLabel(self, text="Масса:").grid(row=3)
        CTkLabel(self, text="Цена:").grid(row=4)
        CTkLabel(self, text="Имя:").grid(row=5)
        CTkLabel(self, text="Фамилия:").grid(row=6)
        CTkLabel(self, text="Дата:").grid(row=7)
        
        val = self.register(validate_float_input)

        self.item_name = CTkEntry(self, placeholder_text="Алмаз")
        self.item_name.insert(0, self.item.item_name)
        self.item_name.grid(row=0, column=1)
        
        self.type_of_item = CTkEntry(self, placeholder_text="Драг камень")
        self.type_of_item.insert(0, self.item.type_of_item)
        self.type_of_item.grid(row=1, column=1)


        self.vescar = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.vescar.insert(0, self.item.vescar)
        self.vescar.grid(row=2, column=1)
        
        self.weight = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.weight.insert(0, self.item.weight)
        self.weight.grid(row=3, column=1)
        
        self.price = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.price.insert(0, self.item.price)
        self.price.grid(row=4, column=1)
        
        self.first_name = CTkEntry(self, placeholder_text="Иван")
        self.first_name.insert(0, self.item.first_name)
        self.first_name.grid(row=5, column=1)
        
        self.surname = CTkEntry(self, placeholder_text="Иванов")
        self.surname.insert(0, self.item.surname)
        self.surname.grid(row=6, column=1)
        
        self.apply_button = CTkButton(self, text="Сохранить", command=self.apply)
        self.apply_button.grid(row=8, column=1)


    def apply(self):
        
        self.item.item_name = self.item_name.get()
        self.item.type_of_item = self.type_of_item.get()
        self.item.vescar = self.vescar.get()
        self.item.weight = self.weight.get()
        self.item.price = self.price.get()
        self.item.first_name = self.price.get()
        self.item.surname = self.price.get()
        
        loop.run_until_complete(self.item.save())
        if self.on_finish:
            self.on_finish()
            
        self.destroy()
        

class CreateDialog(CTk):
    def __init__(self, on_finish=None):
        self.on_finish = on_finish
        super().__init__()
        self.geometry("380x340")
        self.resizable(False, False)

        self.title("Редактирование пользователя")
        CTkLabel(self, text="Наименование товара:").grid(row=0)
        CTkLabel(self, text="металл/драг. камень: ").grid(row=1)
        CTkLabel(self, text="Караты/Проба:").grid(row=2)
        CTkLabel(self, text="Масса:").grid(row=3)
        CTkLabel(self, text="Цена:").grid(row=4)
        CTkLabel(self, text="Имя:").grid(row=5)
        CTkLabel(self, text="Фамилия:").grid(row=6)
        CTkLabel(self, text="Дата:").grid(row=7)
        
        val = self.register(validate_float_input)


        self.item_name = CTkEntry(self, placeholder_text="Алмаз")
        self.item_name.grid(row=0, column=1)
        
        self.type_of_item = CTkEntry(self, placeholder_text="Драг камень")
        self.type_of_item.grid(row=1, column=1)

        
        self.vescar = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.vescar.grid(row=2, column=1)
        
        self.weight = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.weight.grid(row=3, column=1)
        
        self.price = CTkEntry(self, validate="key", validatecommand=(val, '%P'), placeholder_text="10.0")
        self.price.grid(row=4, column=1)
        
        self.first_name = CTkEntry(self, placeholder_text="Иван")
        self.first_name.grid(row=5, column=1)
        
        self.surname = CTkEntry(self, placeholder_text="Иванов")
        self.surname.grid(row=6, column=1)
        
        self.apply_button = CTkButton(self, text="Сохранить", command=self.apply)
        self.apply_button.grid(row=7, column=1)


    def apply(self):
        
        loop.run_until_complete(Items.create(
            item_name=self.item_name.get(),
            type_of_item=self.type_of_item.get(), 
            vescar=self.vescar.get(),
            weight=self.weight.get(),
            price=self.price.get(),
            first_name=self.first_name.get(),
            surname=self.surname.get(),
            ))  

        if self.on_finish:
            self.on_finish()
            
        self.destroy()
        
        
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
    
