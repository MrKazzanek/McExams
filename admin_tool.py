import customtkinter as ctk
import json
import os
from tkinter import messagebox

class McExamsAdmin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("McExams - Panel Administratora")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.questions = []
        self.load_questions()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(2, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="McExams Admin", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_btn = ctk.CTkButton(self.sidebar, text="Dodaj Pytanie", command=self.add_question_ui)
        self.add_btn.grid(row=1, column=0, padx=20, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="Lista Pytań")
        self.scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)

        self.init_main_ui()
        self.refresh_list()

    def load_questions(self):
        path = 'data/questions.json'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
        else:
            self.questions = []

    def save_questions(self):
        path = 'data/questions.json'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Sukces", "Baza pytań została zapisana!")

    def init_main_ui(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        self.welcome_label = ctk.CTkLabel(self.main_content, text="Wybierz pytanie z listy lub dodaj nowe", font=ctk.CTkFont(size=18))
        self.welcome_label.pack(expand=True)

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for i, q in enumerate(self.questions):
            btn = ctk.CTkButton(self.scroll_frame, text=f"{i+1}. {q['question'][:30]}...", 
                                fg_color="transparent", anchor="w",
                                command=lambda q=q: self.edit_question_ui(q))
            btn.pack(fill="x", pady=2)

    def add_question_ui(self):
        new_q = {
            "id": max([q['id'] for q in self.questions] + [0]) + 1,
            "type": "abcd",
            "question": "",
            "options": ["", "", "", ""],
            "answer": ""
        }
        self.edit_question_ui(new_q, is_new=True)

    def edit_question_ui(self, q, is_new=False):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        title = "Dodaj Nowe Pytanie" if is_new else "Edytuj Pytanie"
        ctk.CTkLabel(self.main_content, text=title, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Question Text
        ctk.CTkLabel(self.main_content, text="Treść pytania:").pack(padx=20, anchor="w")
        q_entry = ctk.CTkTextbox(self.main_content, height=100)
        q_entry.pack(fill="x", padx=20, pady=5)
        q_entry.insert("1.0", q['question'])

        # Type
        type_var = ctk.StringVar(value=q['type'])
        ctk.CTkLabel(self.main_content, text="Typ pytania:").pack(padx=20, anchor="w")
        type_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        type_frame.pack(fill="x", padx=20)
        
        def toggle_options():
            if type_var.get() == "tf":
                opt_frame.pack_forget()
                tf_frame.pack(fill="x", padx=20, pady=10)
            else:
                tf_frame.pack_forget()
                opt_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkRadioButton(type_frame, text="ABCD", variable=type_var, value="abcd", command=toggle_options).pack(side="left", padx=10)
        ctk.CTkRadioButton(type_frame, text="Prawda/Fałsz", variable=type_var, value="tf", command=toggle_options).pack(side="left", padx=10)

        # Options ABCD
        opt_frame = ctk.CTkFrame(self.main_content)
        entries = []
        for i in range(4):
            f = ctk.CTkFrame(opt_frame, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{chr(65+i)}:").pack(side="left", padx=5)
            e = ctk.CTkEntry(f)
            e.pack(side="left", fill="x", expand=True, padx=5)
            if q['type'] == 'abcd':
                e.insert(0, q['options'][i])
            entries.append(e)

        # Options TF
        tf_frame = ctk.CTkFrame(self.main_content)
        tf_var = ctk.StringVar(value=q['answer'] if q['type'] == 'tf' else "Prawda")
        ctk.CTkRadioButton(tf_frame, text="Prawda", variable=tf_var, value="Prawda").pack(side="left", padx=20)
        ctk.CTkRadioButton(tf_frame, text="Fałsz", variable=tf_var, value="Fałsz").pack(side="left", padx=20)

        # Answer ABCD
        ans_label = ctk.CTkLabel(opt_frame, text="Poprawna odpowiedź (wpisz tekst identyczny z jedną z opcji):")
        ans_label.pack(padx=20, anchor="w", pady=(10, 0))
        ans_entry = ctk.CTkEntry(opt_frame)
        ans_entry.pack(fill="x", padx=20, pady=5)
        if q['type'] == 'abcd':
            ans_entry.insert(0, q['answer'])

        # Explanation
        ctk.CTkLabel(self.main_content, text="Wytłumaczenie (widoczne po egzaminie):").pack(padx=20, anchor="w", pady=(10, 0))
        exp_entry = ctk.CTkTextbox(self.main_content, height=80)
        exp_entry.pack(fill="x", padx=20, pady=5)
        exp_entry.insert("1.0", q.get('explanation', ''))

        if q['type'] == 'tf':
            opt_frame.pack_forget()
            tf_frame.pack(fill="x", padx=20, pady=10)
        else:
            opt_frame.pack(fill="x", padx=20, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        def save():
            q['question'] = q_entry.get("1.0", "end-1c")
            q['type'] = type_var.get()
            q['explanation'] = exp_entry.get("1.0", "end-1c")
            if q['type'] == 'abcd':
                q['options'] = [e.get() for e in entries]
                q['answer'] = ans_entry.get()
            else:
                q['options'] = ["Prawda", "Fałsz"]
                q['answer'] = tf_var.get()
            
            if is_new:
                self.questions.append(q)
            
            self.save_questions()
            self.refresh_list()
            self.init_main_ui()

        ctk.CTkButton(btn_frame, text="Zapisz", command=save, fg_color="green", hover_color="darkgreen").pack(side="left", padx=10)
        
        if not is_new:
            def delete():
                if messagebox.askyesno("Usuń", "Czy na pewno chcesz usunąć to pytanie?"):
                    self.questions.remove(q)
                    self.save_questions()
                    self.refresh_list()
                    self.init_main_ui()
            ctk.CTkButton(btn_frame, text="Usuń", command=delete, fg_color="red", hover_color="darkred").pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="Anuluj", command=self.init_main_ui).pack(side="right", padx=10)

if __name__ == "__main__":
    app = McExamsAdmin()
    app.mainloop()
