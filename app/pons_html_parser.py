from html.parser import HTMLParser
import tkinter as tk

class SimpleHTMLParser(HTMLParser):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.current_tags = []

        # Configure basic styles
        self.text_widget.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        self.text_widget.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        self.text_widget.tag_configure("underline", underline=True)
        self.text_widget.tag_configure("phonetics", foreground="blue")
        self.text_widget.tag_configure("wordclass", foreground="green")
        self.text_widget.tag_configure("flexion", foreground="purple")
        self.text_widget.tag_configure("genus", foreground="brown")
        self.text_widget.tag_configure("verbclass", foreground="orange")
        self.text_widget.tag_configure("topic", foreground="teal")
        self.text_widget.tag_configure("style", foreground="darkgreen")
        self.text_widget.tag_configure("info", foreground="gray")
        self.text_widget.tag_configure("collocator", foreground="darkblue")
        self.text_widget.tag_configure("rhetoric", foreground="pink")
        self.text_widget.tag_configure("restriction", foreground="darkred")
        self.text_widget.tag_configure("example", foreground="navy")
        self.text_widget.tag_configure("full_collocation", foreground="maroon")
        self.text_widget.tag_configure("idiom_proverb", foreground="purple")
        self.text_widget.tag_configure("case", foreground="olive")
        self.text_widget.tag_configure("zphrase", foreground="cyan")
        self.text_widget.tag_configure("zpinyin", foreground="cyan", font=("TkDefaultFont", 9))
        self.text_widget.tag_configure("pyu", foreground="cyan", font=("TkDefaultFont", 9))
        self.text_widget.tag_configure("separator", foreground="gray")
        self.text_widget.tag_configure("sup", offset=4, font=("TkDefaultFont", 8))
        self.text_widget.tag_configure("sub", offset=-2, font=("TkDefaultFont", 8))
        self.text_widget.tag_configure("acronym", font=("TkDefaultFont", 10, "italic"))

    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self.current_tags.append("bold")
        elif tag in ("i", "em"):
            self.current_tags.append("italic")
        elif tag == "u":
            self.current_tags.append("underline")
        elif tag == "sup":
            self.current_tags.append("sup")
        elif tag == "sub":
            self.current_tags.append("sub")
        elif tag == "acronym":
            self.current_tags.append("acronym")
        elif tag == "br":
            self.text_widget.insert(tk.END, "\n")
        elif tag == "span":
            for name, value in attrs:
                mapping = {
                    "phonetics": "phonetics",
                    "wordclass": "wordclass",
                    "flexion": "flexion",
                    "genus": "genus",
                    "verbclass": "verbclass",
                    "topic": "topic",
                    "style": "style",
                    "info": "info",
                    "collocator": "collocator",
                    "rhetoric": "rhetoric",
                    "restriction": "restriction",
                    "example": "example",
                    "full_collocation": "full_collocation",
                    "idiom_proverb": "idiom_proverb",
                    "case": "case",
                    "zphrase": "zphrase",
                    "zpinyin": "zpinyin",
                    "pyu": "pyu",
                    "separator": "separator"
                }
                if value in mapping:
                    self.current_tags.append(mapping[value])

    def handle_endtag(self, tag):
        if tag in ("strong", "i", "em", "u", "span", "sup", "sub", "acronym"):
            if self.current_tags:
                self.current_tags.pop()

    def handle_data(self, data):
        self.text_widget.insert(tk.END, data, self.current_tags)