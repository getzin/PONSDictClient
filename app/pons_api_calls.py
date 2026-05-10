import requests
import json

# https://en.pons.com/open_dict/public_api
# https://de.pons.com/p/files/uploads/pons/api/api-documentation.pdf

# https://translate-api.pons.com/docs#/TextTranslationApiV1/v1Translate
# https://api.pons.com/v1/dictionary?l=deen&q=house

# API key: XXX
# curl -v --header "X-Secret: XXX" "https://api.pons.com/v1/dictionary?l=deen&q=house"

# https://jsoncrack.com/editor


# PARAMS
# q -- Request-Parameter Search term (URL-escaped UTF-8)
# l -- Request-Parameter Dictionary (i.e. deen,deru) - consult the search url on the result page of a search (on our website). Note: This does not imply a direction, i.e. 'deen' may yield results in both german->english and english->german directions. To specify a direction, use the in-parameter.
# in -- Request-Parameter [optional] Specify the source language (the language of the search term)
# fm -- Request-Parameter [optional] Setting fm=1 enables fuzzy matching
# ref -- Request-Parameter [optional, recommended] Setting ref=true enables references. See section "References" for info.
# language -- Request-Parameter [optional] The language of the output (ISO 639-1 - two-letter codes). Supported languages are de,el,en,es,fr,it,pl,pt,ru,sl,tr,zh.

# 200 OK Normal condition (results could be found)
# 204 NO CONTENT Normal condition (no results could be found)
# 404 NOT FOUND The dictionary does not exist
# 403 NOT AUTHORIZED * The supplied credentials could not be verified. * The access to a dictionary is not allowed
# 500 INTERNAL SERVER ERROR An internal error has occurred

pons_api_result_string = """
[{"lang":"de","hits":[{"type":"entry","opendict":false,"roms":[{"headword":"Test","headword_full":"Test   <span class=\\"flexion\\">&lt;-[e]s, -s [<span class=\\"or\\"><acronym title=\\"oder\\">o.</acronym></span> -e]&gt;</span>  <span class=\\"phonetics\\">[tɛst]</span> <span class=\\"wordclass\\"><acronym title=\\"Substantiv\\">SUBST</acronym></span> <span class=\\"genus\\"><acronym title=\\"Maskulinum\\">m</acronym></span>","wordclass":"Nomen","arabs":[{"header":"1. Test <span class=\\"sense\\">(Versuch)</span>:","translations":[{"source":"<strong class=\\"headword\\">Test</strong>","target":"test"},{"source":"<span class=\\"full_collocation\\">einen <strong class=\\"tilde\\">Test</strong> machen</span>","target":"to carry out a test"}]},{"header":"2. Test <span class=\\"topic\\"><acronym title=\\"Pharmazie\\">PHARM</acronym></span>:","translations":[{"source":"<strong class=\\"headword\\">Test</strong>","target":"test"},{"source":"<span class=\\"full_collocation\\">einen <strong class=\\"tilde\\">Test</strong> machen</span>","target":"to undergo a test"}]},{"header":"3. Test <span class=\\"topic\\"><acronym title=\\"Schulwesen, Bildung\\">SCHULE</acronym></span>:","translations":[{"source":"<strong class=\\"headword\\">Test</strong>","target":"test"}]}]}]},{"type":"entry","opendict":false,"roms":[{"headword":"tes·ten","headword_full":"tes<span class=\\"separator\\">·</span>ten  <span class=\\"phonetics\\">[ˈtɛstn̩]</span> <span class=\\"wordclass\\"><acronym title=\\"Verb\\">VERB</acronym></span> <span classs=\\"verbclass\\"><acronym title=\\"transitives Verb\\">trans</acronym></span>","wordclass":"Transitives Verb","arabs":[{"header":"","translations":[{"source":"<span class=\\"grammatical_construction\\"><acronym title=\\"jemanden\\">jdn</acronym>/<acronym title=\\"etwas\\">etw</acronym> [auf <acronym title=\\"etwas\\">etw</acronym> <span class=\\"case\\"><acronym title=\\"Akkusativ\\">Akk</acronym></span>] <strong class=\\"tilde\\">testen\\n</strong>               </span>","target":"to test <acronym title=\\"somebody\\">sb</acronym>/<acronym title=\\"something\\">sth</acronym> [for <acronym title=\\"something\\">sth</acronym>]"}]}]}]},{"type":"entry","opendict":false,"roms":[{"headword":"HIV-Test","headword_full":"HIV-Test  <span class=\\"phonetics\\">[ha:ʔi:ˈfau-]</span> <span class=\\"wordclass\\"><acronym title=\\"Substantiv\\">SUBST</acronym></span> <span class=\\"genus\\"><acronym title=\\"Maskulinum\\">m</acronym></span>","wordclass":"Nomen","arabs":[{"header":"","translations":[{"source":"<strong class=\\"headword\\">HIV-Test</strong>","target":"HIV test"}]}]}]},{"type":"entry","opendict":false,"roms":[{"headword":"Acid Test","headword_full":"Acid Test    <span class=\\"wordclass\\"><acronym title=\\"Substantiv\\">SUBST</acronym></span> <span class=\\"genus\\"><acronym title=\\"Maskulinum\\">m</acronym></span> <span class=\\"topic\\"><acronym title=\\"Investition und Finanzierung\\">INV-FIN</acronym></span>","wordclass":"Nomen","arabs":[{"header":"","translations":[{"source":"<strong class=\\"headword\\">Acid Test</strong> <span class=\\"sense\\">(Liquiditätsanalyse)</span>","target":"acid test"}]}]}]},{"type":"entry","opendict":false,"roms":[{"headword":"Chi-Quadrat Test","headword_full":"Chi-Quadrat Test    <span class=\\"topic\\"><acronym title=\\"theoretische Modellbildung\\">MODELL</acronym></span>","arabs":[{"header":"","translations":[{"source":"<span class=\\"idiom_proverb\\">Chi-Quadrat Test</span>","target":"Chi square test"}]}]}]}]}]
"""

def status_OK(status_code):
    return (status_code == 200)

import json
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Translation:
    source: str
    target: str

@dataclass
class Arab:
    header: str
    translations: List[Translation]

@dataclass
class Rom:
    headword: str
    headword_full: str
    wordclass: Optional[str] = None
    arabs: List[Arab] = field(default_factory=list)

@dataclass
class Hit:
    type: str
    opendict: bool
    roms: List[Rom] = field(default_factory=list)
    source: Optional[str] = None      # for sentence/example hits
    target: Optional[str] = None
    primary_entry: Optional["Hit"] = None           # for entry_with_secondary_entries
    secondary_entries: List["Hit"] = field(default_factory=list)

@dataclass
class LanguageEntry:
    lang: str
    hits: List[Hit]

def parse_translation(t: dict) -> Translation:
    return Translation(source=t["source"], target=t["target"])

def parse_arab(a: dict) -> Arab:
    translations = [parse_translation(t) for t in a.get("translations", [])]
    return Arab(header=a.get("header", ""), translations=translations)

def parse_rom(r: dict) -> Rom:
    arabs = [parse_arab(a) for a in r.get("arabs", [])]
    return Rom(
        headword=r.get("headword", ""),
        headword_full=r.get("headword_full", ""),
        wordclass=r.get("wordclass"),
        arabs=arabs
    )

def parse_hit(h: dict) -> Hit:
    # Normal roms
    roms = [parse_rom(r) for r in h.get("roms", [])]

    # Sentence/example hits
    source = h.get("source")
    target = h.get("target")

    # Entry with secondary entries
    primary_entry = None
    if h.get("primary_entry"):
        primary_entry = parse_hit(h["primary_entry"])
    secondary_entries = [parse_hit(e) for e in h.get("secondary_entries", [])]

    return Hit(
        type=h.get("type", ""),
        opendict=h.get("opendict", False),
        roms=roms,
        source=source,
        target=target,
        primary_entry=primary_entry,
        secondary_entries=secondary_entries
    )

def parse_language_entry(entry: dict) -> LanguageEntry:
    hits = [parse_hit(h) for h in entry.get("hits", [])]
    return LanguageEntry(lang=entry.get("lang", ""), hits=hits)

def load_json_to_objects(json_string: str) -> List[LanguageEntry]:
    data = json.loads(json_string)
    return [parse_language_entry(entry) for entry in data]

pons_api_json = ""

def search_for_term(search_term, from_lang="de", to_lang="en", display_lang="en"):
    """
    Search the PONS API for a term with specified source (from_lang) and target (to_lang) languages.
    Dictionary code ('l' parameter) is generated by sorting language codes alphabetically.
    """

    # Sort the language codes alphabetically for the dictionary code
    dict_code = "".join(sorted([from_lang, to_lang]))

    param = {
        'q': search_term,
        'l': dict_code,
        'in': from_lang,
        'fm': '0',
        'ref': 'true',
        'language': display_lang,
    }

    header = {
        'X-Secret': '', # Insert your API Key here
    }

    response = requests.get(
        url="https://api.pons.com/v1/dictionary",
        params=param,
        headers=header
    )

    print("----------")
    print("Dictionary code used:", dict_code)
    print(response.text)
    print("----------")

    return response

def get_api_response(search_term, from_lang="de", to_lang="en", display_lang="en"):
    """
    Search PONS API for a term.
    Dictionary code is alphabetical order of from/to languages.
    'display_lang' determines language of output (tooltips, interface text, etc.).
    """

    print("In get_api_response")
    print("Search term:", search_term)
    print("From language:", from_lang)
    print("To language:", to_lang)
    print("Display langauge:", display_lang)

    pons_api_json = ""

    # Change to `if 1:` to enable live API call
    if 1:
        print("Get JSON from API!")
        # Assuming your actual API function accepts search_term, from_lang, to_lang
        pons_api_call = search_for_term(search_term, from_lang, to_lang, display_lang)

        print("START: PRINT API RESPONSE")
        print(pons_api_call)
        print("END: PRINT API RESPONSE")

        if not status_OK(pons_api_call.status_code):
            print("Status Code != 200, received:", pons_api_call.status_code)
            print("(0) type of pons_api_call.text:", type(pons_api_call.text))
            print(pons_api_call.text)
            #print("EXITING...")
            #exit(-1)

        print("-"*30)
        print("START: PRINT API TEXT")
        print("(1) type of pons_api_call.text:", type(pons_api_call.text))
        pons_api_call_text = pons_api_call.text
        print(pons_api_call_text)
        print("END: PRINT API TEXT")
        return pons_api_call_text

    else:
        print("Use pre-determined JSON (test mode)")
        return pons_api_result_string

if __name__ == "__main__":
    result = get_api_response("test")
    print("*"*30)
    print(result)