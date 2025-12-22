from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
import sqlite3
from datetime import datetime


# إنشاء قاعدة البيانات
def initialize_database():
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# حفظ البيانات
def save_to_database(worker_id, action):
    conn = sqlite3.connect('workers.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO attendance (worker_id, action, timestamp) VALUES (?, ?, ?)",
        (worker_id, action, timestamp)
    )
    conn.commit()
    conn.close()


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # الوقت
        self.time_label = Label(
            text="",
            font_size=22,
            color=(1, 0, 0, 1)
        )
        self.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)

        # إدخال رقم العامل
        self.add_widget(Label(text="Identifiant de l'employé :", font_size=16))
        self.worker_input = TextInput(
            multiline=False,
            font_size=16,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.worker_input)

        # زر الدخول
        btn_in = Button(
            text="Enregistrer l'entrée",
            font_size=16,
            background_color=(1, 0, 1, 1),
            size_hint_y=None,
            height=60
        )
        btn_in.bind(on_press=self.check_in)
        self.add_widget(btn_in)

        # زر الخروج
        btn_out = Button(
            text="Enregistrer la sortie",
            font_size=16,
            background_color=(0.96, 0.64, 0.38, 1),
            size_hint_y=None,
            height=60
        )
        btn_out.bind(on_press=self.check_out)
        self.add_widget(btn_out)

        # توقيع
        self.add_widget(Label(
            text="Cette application a été programmée et développée par\nM El ARBAJI RACHID",
            font_size=10,
            color=(1, 0, 0, 1)
        ))

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.7, 0.3)
        )
        popup.open()

    def check_in(self, instance):
        worker_id = self.worker_input.text.strip()
        if worker_id:
            save_to_database(worker_id, "Entrée")
            self.show_popup("Succès", "Enregistrement d'entrée réussi!")
            self.worker_input.text = ""
        else:
            self.show_popup("Erreur", "Veuillez entrer l'identifiant de l'employé!")

    def check_out(self, instance):
        worker_id = self.worker_input.text.strip()
        if worker_id:
            save_to_database(worker_id, "Sortie")
            self.show_popup("Succès", "Enregistrement de sortie réussi!")
            self.worker_input.text = ""
        else:
            self.show_popup("Erreur", "Veuillez entrer l'identifiant de l'employé!")


class AttendanceApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    initialize_database()
    AttendanceApp().run()
