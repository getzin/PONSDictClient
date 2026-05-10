# 🗣️ PONS Dictionary Client

A multi-interface dictionary application powered by the **PONS API**. Search for translations across 12 languages using either a **Flask web app**, **Tkinter desktop GUI**, or **command-line interface**.

---

## ✨ Features

### 🌐 Multiple Interfaces
- **Flask Web App** – Modern, browser-based interface with responsive design
- **Tkinter GUI** – Lightweight desktop application
- **Smart Launcher** – Choose your preferred interface on startup
- **CLI Support** – Command-line translation queries

### 🗺️ Language Support
Supports translations between 12 languages with regional indicators:

| Code | Language | Flag |
|------|----------|------|
| de | German | 🇩🇪 |
| en | English | 🇬🇧 |
| es | Spanish | 🇪🇸 |
| fr | French | 🇫🇷 |
| it | Italian | 🇮🇹 |
| pl | Polish | 🇵🇱 |
| pt | Portuguese | 🇵🇹 |
| ru | Russian | 🇷🇺 |
| el | Greek | 🇬🇷 |
| tr | Turkish | 🇹🇷 |
| sl | Slovenian | 🇸🇮 |
| zh | Chinese | 🇨🇳 |

### 🔍 Advanced Search Features
- **Fuzzy Matching** – Find words even with typos
- **Language-Specific Results** – Filter by source/target language
- **Multiple Meanings** – View different word senses (technical, slang, colloquial, etc.)
- **Part-of-Speech Info** – Understand word types (noun, verb, adjective, etc.)
- **Phonetic Transcription** – See pronunciation guides
- **Contextual Usage** – View example phrases and collocations
- **Flexible Display Language** – UI language independent of search languages

### 🛠️ Technical Features
- **Real-time API Integration** – Direct calls to PONS REST API
- **HTML Parsing** – Cleanly extract and present dictionary data
- **Error Handling** – Graceful handling of network issues and empty results
- **Responsive Design** – Works seamlessly on different screen sizes

---

## 📋 Requirements

- **Python 3.7+**
- **PONS API Access** (free, no key required for basic queries)
- See `requirements.txt` for Python dependencies

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
cd PONSDictClient
pip install -r requirements.txt
```

### 2. Run the Application

**Option A – Launcher (Choose Interface):**
```bash
python pons_main.py
```

A launcher window will appear letting you choose between:
- 🌐 Flask Web App
- 🖥️ Tkinter GUI

**Option B – Direct Flask (Web Interface):**
```bash
python -m app.pons_flask
```
Then open `http://localhost:5000/search` in your browser.

**Option C – Direct Tkinter (Desktop GUI):**
```bash
python -c "from app.pons_tkinter import PonsTkApp; app = PonsTkApp(None); app.create_tkinter()"
```

---

## 📁 Project Structure

```
PONSDictClient/
├── pons_main.py                 # Launcher application (choose interface)
│
├── app/
│   ├── pons_api_calls.py       # PONS API integration & data models
│   ├── pons_flask.py           # Flask web app routes & logic
│   ├── pons_tkinter.py         # Tkinter desktop GUI
│   ├── pons_html_parser.py     # HTML parsing utilities
│   ├── pons_translations.py    # UI text translations (12 languages)
│   │
│   ├── static/                 # Web assets
│   │   ├── css/
│   │   │   └── style.css       # Flask app styling
│   │   ├── icons/              # Application icons
│   │   └── (flag images)        # Language flag graphics
│   │
│   ├── templates/              # Flask HTML templates
│   │   └── index.html          # Main search interface
│   │
│   └── flags/                  # Flag image assets
│
└── requirements.txt            # Python dependencies
```

---

## 🖥️ Interface Guide

### Flask Web Interface

1. **Launch** → `python pons_main.py` → Select "Flask Web App"
2. **Configure**:
   - Select **source language** (left dropdown) – the language of your search term
   - Select **target language** (middle dropdown) – the language for translations
   - Select **display language** (right dropdown) – the UI language
3. **Search**:
   - Enter your search term in the search box
   - Click **"Search!"** button
4. **Results**:
   - Multiple entries displayed with word senses
   - Example phrases and collocations shown
   - Phonetic transcriptions included
   - Related words and grammatical info provided

### Tkinter Desktop GUI

1. **Launch** → `python pons_main.py` → Select "Tkinter GUI"
2. **Window appears** with:
   - Search field at top
   - Language dropdowns for source/target
   - Results panel showing dictionary entries
   - Word sense selector (if multiple meanings)
3. **Search**:
   - Type your word/phrase
   - Press Enter or click search button
   - Results populate instantly

### Launcher Window

- **Centered window** with two prominent buttons
- **"Open Flask Web App"** – Starts Flask server and opens browser
- **"Start Tkinter Desktop App"** – Launches native desktop GUI
- Auto-closes when selection is made

---

## 🔧 API Reference

### Core Functions in `pons_api_calls.py`

#### Search for translations
```python
from app.pons_api_calls import search_pons

results = search_pons(
    search_term="hello",
    from_lang="en",      # Source language (optional)
    to_lang="de",        # Target language (optional)
    dictionary="deen",   # Language pair (German-English)
    fuzzy=True,          # Enable fuzzy matching
    display_lang="en"    # UI language for results
)
```

#### Available Dictionaries
- `deen` – German ↔ English
- `deru` – German ↔ Russian
- `dees` – German ↔ Spanish
- `deit` – German ↔ Italian
- `defs` – German ↔ French
- `elet` – Greek ↔ English
- `enel` – English ↔ Greek
- And many more...

### Data Models (Dataclasses)

```python
@dataclass
class Translation:
    source: str      # Original phrase/word
    target: str      # Translated phrase/word

@dataclass
class Arab:         # Meaning/sense section
    header: str     # Sense descriptor
    translations: List[Translation]

@dataclass
class Rom:          # Dictionary entry form
    headword: str   # Main word
    headword_full: str  # Word with grammar info
    wordclass: str  # Part of speech
    arabs: List[Arab]

@dataclass
class Hit:          # Search result entry
    type: str       # "entry", "inflection", etc.
    roms: List[Rom]
```

---

## 🌍 Language Support & Codes

| Code | Language | Display Name |
|------|----------|--------------|
| de | German | Deutsch |
| en | English | English |
| es | Spanish | Español |
| fr | French | Français |
| it | Italian | Italiano |
| pl | Polish | Polski |
| pt | Portuguese | Português |
| ru | Russian | Русский |
| el | Greek | Ελληνικά |
| tr | Turkish | Türkçe |
| sl | Slovenian | Slovenščina |
| zh | Chinese | 中文 |

---

## 📝 Configuration

### Supported PONS API Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search term (required) |
| `l` | string | Dictionary language pair (e.g., "deen") |
| `in` | string | Source language (optional) |
| `fm` | int | Fuzzy matching: 1=enabled, 0=disabled |
| `ref` | bool | Include references: true/false |
| `language` | string | UI language (ISO 639-1) |

### Fuzzy Matching
Enable fuzzy matching to find words with typos:
```python
search_pons("helo", fuzzy=True)  # Finds "hello"
```

---

## 🔐 API Information

- **Provider**: PONS (https://www.pons.com)
- **Endpoint**: `https://api.pons.com/v1/dictionary`
- **Authentication**: No API key required for basic usage
- **Rate Limiting**: Standard rate limits apply
- **Documentation**: [PONS API Documentation](https://en.pons.com/open_dict/public_api)

---

## 🛠️ Development

### Adding a New Language

1. **Add language code to `pons_flask.py`**:
```python
languages = [
    ("xx", "🇵🇹", "Language Name"),  # Add your language
    # ... existing entries
]
```

2. **Add translations in `pons_translations.py`**:
```python
TRANSLATIONS = {
    "xx": {
        "title": "Your App Title",
        "search_label": "Search dictionary:",
        # ... more entries
    },
    # ... existing translations
}
```

3. **Add flag image** to `app/flags/` or `app/static/icons/`

### Customizing Styles

Edit `app/static/css/style.css` to customize:
- Colors and themes
- Font sizes
- Layout spacing
- Button styles
- Responsive breakpoints

### Adding New Templates

1. Create HTML file in `app/templates/`
2. Reference in Flask routes:
```python
return render_template('your_template.html', data=data)
```

---

## 🐛 Troubleshooting

### Connection Issues
**Problem**: "Error fetching results" or timeout
- Check internet connection
- Verify PONS API is accessible
- Try again with a shorter search term

### No Results Found
**Problem**: Search returns empty results
- Try enabling **fuzzy matching** to find similar words
- Verify source/target language combination is valid
- Check that word exists in dictionary

### Flask Port Already in Use
**Problem**: "Address already in use" error
- Find process using port 5000: `netstat -ano | findstr :5000` (Windows)
- Kill process or use different port in `pons_flask.py`

### Tkinter Window Not Displaying
**Problem**: GUI appears blank or doesn't respond
- Check PYTHONPATH includes project root
- Try running: `python pons_main.py`
- Ensure tkinter is installed: `pip install tk`

### Icon Not Loading
**Problem**: Application icon doesn't appear
- Ensure `app/static/icons/dict.ico` exists
- Check file permissions
- Try running without icon flag (app still works)

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web framework for Flask interface |
| `requests` | HTTP requests to PONS API |
| `lxml` | HTML/XML parsing |
| (tkinter) | Built-in for Tkinter GUI |

---

## 📖 Usage Examples

### Web Interface Search
1. Open Flask app
2. Type: "Katze"
3. Set From: German, To: English
4. Click Search
5. View translations: cat, kitten, feline, etc.

### CLI Search
```python
from app.pons_api_calls import search_pons

results = search_pons("house", dictionary="deen")
for hit in results:
    for rom in hit.roms:
        print(f"Headword: {rom.headword}")
        for arab in rom.arabs:
            print(f"  Sense: {arab.header}")
            for trans in arab.translations:
                print(f"    {trans.source} → {trans.target}")
```

### Programmatic API Usage
```python
from app.pons_api_calls import search_pons, HtmlParser

# Search with fuzzy matching
results = search_pons(
    search_term="tst",  # Typo
    dictionary="deen",
    fuzzy=True
)

# Parse HTML content if needed
parser = HtmlParser()
clean_text = parser.clean_html("<strong>Test</strong>")
```

---

## 🎯 Features Overview

| Feature | Flask | Tkinter | CLI |
|---------|-------|---------|-----|
| Search dictionary | ✅ | ✅ | ✅ |
| 12 language pairs | ✅ | ✅ | ✅ |
| Fuzzy matching | ✅ | ✅ | ✅ |
| Multiple meanings | ✅ | ✅ | ✅ |
| Phonetics | ✅ | ✅ | ✅ |
| Example phrases | ✅ | ✅ | ✅ |
| Responsive UI | ✅ | - | - |
| Offline support | ❌ | ❌ | ❌ |
| Dark mode | - | - | - |

---

## 📄 License

This project uses the PONS API which is provided by PONS GmbH. See PONS terms of service for restrictions.

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional language support
- Dark mode for web interface
- Offline dictionary caching
- Browser extension
- Mobile app
- Pronunciation audio playback

---

## 🔗 Resources

- [PONS Website](https://www.pons.com)
- [PONS API Documentation](https://en.pons.com/open_dict/public_api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

**Happy translating! 🌍✨**
