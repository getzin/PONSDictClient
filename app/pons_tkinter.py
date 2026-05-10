import sys
import os

# Add parent folder to sys.path so 'app' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk
from json import JSONDecodeError
from app import pons_api_calls
from app import pons_html_parser
from app import pons_translations


class ToolTip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        text = self.text_func()  # get current text dynamically
        if self.tipwindow or not text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("TkDefaultFont", 9))
        label.pack(ipadx=1)

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class LabeledEntry(ttk.Frame):
    def __init__(self, master=None, label_text="", entry_width=20, frame_width=300, frame_height=30, **kwargs):
        super().__init__(master, width=frame_width, height=frame_height, **kwargs)
        self.pack_propagate(False)  # prevent frame from resizing to children
        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self, width=entry_width)
        self.label.pack(side="left", padx=(0, 5), pady=2)
        self.entry.pack(side="left", fill="x", expand=True, pady=2)

    def get(self):
        return self.entry.get()

    def set(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class PonsTkApp:

    def __init__(self, pons_data_in):
        self.window = tk.Tk()
        self.pons_data = pons_data_in

        self.search_widget = None
        self.app_lang_var = None
        self.from_lang_var = None
        self.to_lang_var = None
        self.app_lang_code = None
        self.from_lang_code = None
        self.to_lang_code = None
        self.flag_images = {}

        self.results_text = None

    def getScreenSize(self):
        temp_window = tk.Tk()
        temp_window.withdraw()
        width = temp_window.winfo_screenwidth()
        height = temp_window.winfo_screenheight()
        temp_window.destroy()
        return width, height

    def t(self, key: str) -> str:
        """Translate string based on app_lang_code, fallback to English."""
        lang = self.app_lang_code or "en"
        lang_dict = pons_translations.TRANSLATIONS.get(
            lang, pons_translations.TRANSLATIONS["en"]
        )
        return lang_dict.get(key, key)

    def display_results(self, entries):
        """Clear and insert entries into bottom Text widget."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        if not entries:
            self.results_text.insert(tk.END, self.t("no_results"))
            self.results_text.config(state="disabled")
            return

        parser = pons_html_parser.SimpleHTMLParser(self.results_text)

        def _display_hit(hit_obj):
            """Helper to display normal hits (roms)."""
            for rom in hit_obj.roms:
                parser.feed(rom.headword_full)
                self.results_text.insert(tk.END, "\n")
                for arab in rom.arabs:
                    if arab.header:
                        parser.feed(arab.header)
                        self.results_text.insert(tk.END, "\n")
                    for t in arab.translations:
                        parser.feed(f"{t.source} → {t.target}\n")
                self.results_text.insert(tk.END, "\n")

        for entry in entries:
            for hit in entry.hits:
                if hasattr(hit, "roms") and hit.roms:  # normal dictionary entries
                    _display_hit(hit)

                elif getattr(hit, "type", None) == "entry_with_secondary_entries":
                    if hasattr(hit, "primary_entry") and hit.primary_entry:
                        _display_hit(hit.primary_entry)
                    if hasattr(hit, "secondary_entries") and hit.secondary_entries:
                        for sec in hit.secondary_entries:
                            _display_hit(sec)

                elif hasattr(hit, "source") and hasattr(hit, "target"):  # sentence/example
                    parser.feed(f"{hit.source} → {hit.target}\n")
                    self.results_text.insert(tk.END, "\n")

        self.results_text.config(state="disabled")

    def search_submit(self, event=None):
        search_term = self.search_widget.get()
        print("User submitted search:", search_term)

        entries = []
        try:
            search_result = pons_api_calls.get_api_response(
                search_term,
                self.from_lang_code,
                self.to_lang_code,
                self.app_lang_code,
            )
            entries = pons_api_calls.load_json_to_objects(search_result)
        except JSONDecodeError as e:
            # Handle JSON parsing errors separately
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                tk.END, f"{self.t('error_json')}\n{e}"
            )
            self.results_text.config(state="disabled")
            self.search_widget.entry.focus_set()
            return
        except Exception as e:
            # All other errors (API, network, etc.)
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                tk.END, f"{self.t('error_fetch')}\n{e}"
            )
            self.results_text.config(state="disabled")
            self.search_widget.entry.focus_set()
            return

        self.search_widget.entry.focus_set()
        self.display_results(entries)

    def update_search_state(self):
        if self.from_lang_code and self.to_lang_code:
            self.search_widget.entry.config(state="normal")
            self.search_button.config(state="normal")
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, self.t("enter_word"))
            self.results_text.config(state="disabled")
        else:
            self.search_widget.entry.config(state="disabled")
            self.search_button.config(state="disabled")
            self.results_text.config(state="normal")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, self.t("please_select"))
            self.results_text.config(state="disabled")
        return

    def update_language_dropdowns(self):
        """Refresh From/To dropdowns with current app_lang translations."""
        self.build_from_lang_menu()
        self.build_to_lang_menu()

    def update_ui_language(self):
        """Refresh UI text when display language changes."""
        self.window.title(self.t("title"))
        self.search_widget.label.config(text=self.t("search_label"))
        self.search_button.config(text=self.t("search_button"))

        self.update_search_state()
        self.update_language_dropdowns()

    # ---- Dropdown builders ----
    def build_app_lang_menu(self, parent, lang_codes):
        container = tk.Frame(parent, width=120, height=30)
        container.pack(side="left", padx=2)
        container.pack_propagate(False)

        mb = tk.Menubutton(container, text=self.t("display_lang"), relief="raised", compound="left")
        mb.pack(fill="both", expand=True)
        menu = tk.Menu(mb, tearoff=0)
        container.menu = menu
        mb.config(menu=menu)

        # display-language names are always shown in English list (so people can pick)
        lang_dict = pons_translations.TRANSLATIONS["en"]["languages"]
        sorted_codes = sorted(lang_codes, key=lambda c: lang_dict[c])

        for code in sorted_codes:
            name = lang_dict[code]
            img = self.flag_images.get(code)

            # capture img, code, name in defaults to avoid late-binding bug
            def cmd(c=code, n=name, i=img):
                self.app_lang_var.set(n)
                self.app_lang_code = c
                mb.config(text=n, image=i)
                self.update_ui_language()

            menu.add_command(label=name, image=img, compound="left", command=cmd)

        mb.config(bg="#d9f0ff")
        return container

    def build_from_lang_menu(self):
        mb = self.from_lang_frame.winfo_children()[0]
        menu = self.from_lang_frame.menu
        menu.delete(0, tk.END)

        lang_dict = pons_translations.TRANSLATIONS[self.app_lang_code]["languages"]
        sorted_codes = sorted(lang_dict.keys(), key=lambda c: lang_dict[c])

        for code in sorted_codes:
            name = lang_dict[code]
            img = self.flag_images.get(code)

            # capture img, code, name
            def cmd(c=code, n=name, i=img):
                self.from_lang_var.set(n)
                self.from_lang_code = c
                mb.config(text=n, image=i)
                self.update_search_state()

            menu.add_command(label=name, image=img, compound="left", command=cmd)

        if self.from_lang_code:
            mb.config(
                text=lang_dict.get(self.from_lang_code, self.from_lang_code),
                image=self.flag_images.get(self.from_lang_code),
            )
        else:
            mb.config(text=self.t("from_label"), image="")

    def build_to_lang_menu(self):
        mb = self.to_lang_frame.winfo_children()[0]
        menu = self.to_lang_frame.menu
        menu.delete(0, tk.END)

        lang_dict = pons_translations.TRANSLATIONS[self.app_lang_code]["languages"]
        sorted_codes = sorted(lang_dict.keys(), key=lambda c: lang_dict[c])

        for code in sorted_codes:
            name = lang_dict[code]
            img = self.flag_images.get(code)

            # capture img, code, name
            def cmd(c=code, n=name, i=img):
                self.to_lang_var.set(n)
                self.to_lang_code = c
                mb.config(text=n, image=i)
                self.update_search_state()

            menu.add_command(label=name, image=img, compound="left", command=cmd)

        if self.to_lang_code:
            mb.config(
                text=lang_dict.get(self.to_lang_code, self.to_lang_code),
                image=self.flag_images.get(self.to_lang_code),
            )
        else:
            mb.config(text=self.t("to_label"), image="")

    def setup_window(self):
        """Setup main window and frames, center on screen."""
        self.window.title(self.t("title"))

        self.window.geometry("900x600")
        self.window.minsize(900, 600)

        # Center window
        screen_width, screen_height = self.getScreenSize()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.window.geometry(f"900x600+{x}+{y}")

        # Create top and bottom frames
        self.top_frame = ttk.Frame(self.window, padding=5)
        self.bottom_frame = ttk.Frame(self.window)
        self.top_frame.pack(fill="x")
        self.bottom_frame.pack(fill="both", expand=True)

        # --- Set custom icon ---
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "static", "icons", "dict.ico")
            icon_path = os.path.abspath(icon_path).replace("\\", "/")
            self.window.iconbitmap(icon_path)
        except tk.TclError:
            print(f"Failed to load icon: {icon_path}")

    def setup_results_text(self, bottom_frame):
        """Setup Text widget for displaying results and scrollbar."""
        scrollbar = ttk.Scrollbar(bottom_frame)
        self.results_text = tk.Text(
            bottom_frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("TkDefaultFont", 11),
            padx=5,
            pady=5,
        )
        scrollbar.config(command=self.results_text.yview)
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.results_text.config(state="disabled")

    def load_flags(self):
        """Load flag images from /flags folder."""
        lang_names = {
            "de": "German",
            "el": "Greek",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "it": "Italian",
            "pl": "Polish",
            "pt": "Portuguese",
            "ru": "Russian",
            "sl": "Slovenian",
            "tr": "Turkish",
            "zh": "Chinese",
        }
        script_dir = os.path.dirname(os.path.abspath(__file__))
        flags_dir = os.path.join(script_dir, "flags")

        for code in lang_names:
            path = os.path.join(flags_dir, f"{code}.png")
            if os.path.exists(path):
                self.flag_images[code] = tk.PhotoImage(file=path)
            else:
                self.flag_images[code] = None

    def setup_display_language_dropdown(self, top_frame):
        """Setup the display language Menubutton with tooltip."""
        lang_names = sorted(
            ["de","el","en","es","fr","it","pl","pt","ru","sl","tr","zh"],
            key=lambda x: pons_translations.TRANSLATIONS["en"]["languages"][x]
        )
        display_dropdown_frame = self.build_app_lang_menu(top_frame, lang_names)
        self.app_lang_var.set("English")
        self.app_lang_code = "en"
        mb = display_dropdown_frame.winfo_children()[0]
        mb.config(text="English", image=self.flag_images.get("en"))
        display_dropdown_frame.pack(side="left", padx=(0, 10))
        ToolTip(mb, lambda: self.t("tooltip_display_lang"))

    def setup_search_widgets(self, top_frame):
        """Setup search label+entry and search button."""
        self.search_widget = LabeledEntry(
            top_frame, label_text=self.t("search_label"), entry_width=30, frame_width=350
        )
        self.search_widget.pack(side="left", padx=(5, 10))
        self.search_widget.entry.configure(font=("TkDefaultFont", 12))
        self.search_widget.entry.bind("<Return>", self.search_submit)

        style = ttk.Style()
        style.configure(
            "Rect.TButton",
            relief="flat",
            borderwidth=1,
            padding=(1, 5),
            anchor="center",
        )

        self.search_button = ttk.Button(
            top_frame,
            text=self.t("search_button"),
            command=self.search_submit,
            style="Rect.TButton",
        )
        self.search_button.pack(side="left", padx=(5, 10), fill="y")

        self.search_widget.entry.config(state="disabled")
        self.search_button.config(state="disabled")

    def setup_from_to_dropdowns(self, top_frame):
        """Setup From and To dropdowns and the arrow label."""
        dropdown_frame = ttk.Frame(top_frame)
        dropdown_frame.pack(side="right")

        # FROM frame
        self.from_lang_frame = tk.Frame(dropdown_frame, width=120, height=30)
        self.from_lang_frame.pack(side="left", padx=2)
        self.from_lang_frame.pack_propagate(False)
        mb_from = tk.Menubutton(
            self.from_lang_frame,
            text=self.t("from_label"),
            relief="raised",
            compound="left",
            bg="#d4f8d4",
            activebackground="#a6f1a6"
        )
        mb_from.pack(fill="both", expand=True)
        menu_from = tk.Menu(mb_from, tearoff=0)
        self.from_lang_frame.menu = menu_from
        mb_from.config(menu=menu_from)
        ToolTip(mb_from, lambda: self.t("tooltip_from_lang"))

        arrow_label = ttk.Label(dropdown_frame, text="→")
        arrow_label.pack(side="left", padx=2)

        # TO frame
        self.to_lang_frame = tk.Frame(dropdown_frame, width=120, height=30)
        self.to_lang_frame.pack(side="left", padx=2)
        self.to_lang_frame.pack_propagate(False)
        mb_to = tk.Menubutton(
            self.to_lang_frame,
            text=self.t("to_label"),
            relief="raised",
            compound="left",
            bg="#f8d4d4",
            activebackground="#f1a6a6"
        )
        mb_to.pack(fill="both", expand=True)
        menu_to = tk.Menu(mb_to, tearoff=0)
        self.to_lang_frame.menu = menu_to
        mb_to.config(menu=menu_to)
        ToolTip(mb_to, lambda: self.t("tooltip_to_lang"))

    def create_tkinter(self):
        self.app_lang_var = tk.StringVar()
        self.from_lang_var = tk.StringVar()
        self.to_lang_var = tk.StringVar()

        self.setup_window()
        self.setup_results_text(self.bottom_frame)
        self.load_flags()
        self.setup_display_language_dropdown(self.top_frame)
        self.setup_search_widgets(self.top_frame)
        self.setup_from_to_dropdowns(self.top_frame)
        self.update_search_state()
        self.update_language_dropdowns()
        self.window.mainloop()


if __name__ == "__main__":
    tmp = PonsTkApp(None)
    tmp.create_tkinter()
