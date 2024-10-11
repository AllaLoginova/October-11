import tkinter as tk
import json

class SingletonMeta(type):
    """
    EN: The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.

    RU: В Python класс Одиночка можно реализовать по-разному. Возможные
    способы включают себя базовый класс, декоратор, метакласс. Мы воспользуемся
    метаклассом, поскольку он лучше всего подходит для этой цели.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        EN: Possible changes to the value of the `__init__` argument do not
        affect the returned instance.

        RU: Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class NoteWindow:
    def __init__(self, model):
        self.model = model
        self.create_window()
        self.show_notes()
        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title('Заметки')

        # ввод
        self.input = tk.Text(self.root, height=10, width=20)
        self.input.grid(row=0, column=0, padx=10, pady=10)

        # вывод
        self.output = tk.Listbox(self.root, height=10, width=20)
        self.output.grid(row=0, column=1, padx=10, pady=10)

        self.button = tk.Button(self.root, text='Добавить заметку', command=self.add_note)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def add_note(self):
        text = self.input.get('1.0', tk.END)
        self.model.add_note(text)
        self.show_notes()

        self.input.delete('1.0', tk.END)

    def show_notes(self):
        notes = self.model.get_notes()
        self.output.delete(0, tk.END)
        for note in notes:
            self.output.insert(tk.END, note['text'])


class NoteModel(metaclass=SingletonMeta):
    """База данных для хранения заметок"""
    def __init__(self):
        self._notes = self._load_from_file()
        self.observers = []

    def get_notes(self):
        return self._notes

    def add_note(self, text):
        next_id = self._get_last_id() + 1 # получаем новый id
        note = {"id": next_id, "text": text} # создаем заметку
        self._notes.append(note) # добавляем в список
        self.save_to_file()

        self.update_notifiers(text)

    def delete_by_id(self, note_id):
        for number, note in enumerate(self._notes):
            if note['id'] == note_id:
                self._notes.pop(number)
                break
        else:
            print('Такой заметки нет')

    def find_by_text(self, text_to_find):
        res = []
        for note in self._notes:
            if text_to_find in note['text']:
                res.append(note)
        return res

    def attach_observers(self, observer):
        self.observers.append(observer)

    def update_notifiers(self, text):
        for observer in self.observers:
            observer.update(text)

    def _load_from_file(self):
        """Загрузка данных из файла"""
        with open('notes.json', 'r', encoding='utf-8') as f:
            notes = json.load(f)
        return notes

    def save_to_file(self):
        with open('notes.json', 'w', encoding='utf-8') as f:
            notes = json.dump(self._notes, f)
        return notes

    def _get_last_id(self):
        """ """
        if self._notes:
            max = self._notes[0]['id']
            for note in self._notes:
                if note['id'] > max:
                    max = note['id']
        else:
            max = 0

        return max

class EmailNotifer:
    @staticmethod
    def update(text):
        print(f"Добавилась заметка с текстом {text}")


class SMSNotifier:
    @staticmethod
    def update(text):
        print(f"Добавилась SMS с текстом {text}")

class AuthDecorator:     # декоратор
    def __init__(self, notirier):
        self.notirier = notirier

    def update(self, text):
        password = input('Введи пароль ')
        if password == '123':
            self.notirier.update(text)
        else:
            print('Пароль не правильный')

model = NoteModel()

email = EmailNotifer()
email_auth = AuthDecorator(email)
sms = SMSNotifier()

model.attach_observers(email_auth)
model.attach_observers(sms)


window = NoteWindow(model)
