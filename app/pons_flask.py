import sys
import os

# Add parent folder to sys.path so 'app' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
from app import pons_api_calls

languages = [
    ("de", "🇩🇪", "German"),
    ("el", "🇬🇷", "Greek"),
    ("en", "🇬🇧", "English"),
    ("es", "🇪🇸", "Spanish"),
    ("fr", "🇫🇷", "French"),
    ("it", "🇮🇹", "Italian"),
    ("pl", "🇵🇱", "Polish"),
    ("pt", "🇵🇹", "Portuguese"),
    ("ru", "🇷🇺", "Russian"),
    ("sl", "🇸🇮", "Slovenian"),
    ("tr", "🇹🇷", "Turkish"),
    ("zh", "🇨🇳", "Chinese")
]

app = Flask(__name__)

def create_routes(flask_app):
    """Register all routes to the given Flask app."""

    @flask_app.route("/search", methods=["GET", "POST"])
    def display_search():
        print("display_search!")
        entries = []
        search_term = ""
        from_lang = "en"  # default source language
        to_lang = "de"    # default target language
        display_lang = "en"  # default display language

        if request.method == "POST":
            search_term = request.form.get("search_term", "").strip()
            from_lang = request.form.get("from_language", from_lang)
            to_lang = request.form.get("to_language", to_lang)
            display_lang = request.form.get("display_language", display_lang)

            if search_term:
                print("Search term:", search_term)
                print("From language:", from_lang)
                print("To language:", to_lang)
                print("Display language:", display_lang)

                try:
                    result = pons_api_calls.get_api_response(
                        search_term, from_lang, to_lang, display_lang
                    )
                    print("+"*30)
                    print(result)
                    entries = pons_api_calls.load_json_to_objects(result)
                    print("~"*30)
                except Exception as e:
                    print("Error parsing JSON:", e)
            else:
                print("No search term.")
        else:
            print("No POST request.")

        return render_template(
            "index.html",
            entries=entries,
            search_term=search_term,
            from_lang=from_lang,
            to_lang=to_lang,
            display_lang=display_lang,
            languages=languages
        )

def run_flask(use_reloader=True):
    """
    Start the Flask server.

    Args:
        use_reloader (bool): Whether to enable the Flask reloader.
                             True if running directly, False if launched from another process.
    """
    create_routes(app)
    app.run(
        host="0.0.0.0",   # make server visible to other devices in the network
        port=5000,        # keep your usual port
        debug=True,
        use_reloader=use_reloader
    )


if __name__ == "__main__":
    run_flask(True)
