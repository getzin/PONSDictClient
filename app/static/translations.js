// Translation object
// \u00A0 is non-breaking space, some languages require it to be typographically correct
const translations = {
    en: {
        title: "Andy's Dictionary App",
        search_label: "Search:",
        from_label: "From:",
        to_label: "To:",
        display_label: "Display language:",
        search_button: "SEARCH 🔍",
        search_results: 'Search results for "{{search_term}}"',
        language_label: "Language:",
        no_results: "No results found.",
        please_enter: "Please enter a search term here..."
    },
    es: {
        title: "Aplicación de diccionario de Andy",
        search_label: "Buscar:",
        from_label: "De:",
        to_label: "A:",
        display_label: "Idioma de la interfaz:",
        search_button: "BUSCAR 🔍",
        search_results: 'Resultados de búsqueda para "{{search_term}}"',
        language_label: "Idioma:",
        no_results: "No se encontraron resultados.",
        please_enter: "Por favor ingrese un término de búsqueda aquí..."
    },
    fr: {
        title: "Application de dictionnaire d'Andy",
        search_label: "Rechercher\u00A0:",
        from_label: "De\u00A0:",
        to_label: "Vers\u00A0:",
        display_label: "Langue d’affichage\u00A0:",
        search_button: "RECHERCHER 🔍",
        search_results: 'Résultats de recherche pour «\u00A0{{search_term}}\u00A0»',
        language_label: "Langue\u00A0:",
        no_results: "Aucun résultat trouvé.",
        please_enter: "Veuillez entrer un terme de recherche ici..."
    },
    de: {
        title: "Andys Wörterbuch-App",
        search_label: "Suche:",
        from_label: "Von:",
        to_label: "Nach:",
        display_label: "Anzeigesprache:",
        search_button: "SUCHEN 🔍",
        search_results: 'Suchergebnisse für „{{search_term}}“',
        language_label: "Sprache:",
        no_results: "Keine Ergebnisse gefunden.",
        please_enter: "Bitte geben Sie hier einen Suchbegriff ein..."
    },
    el: {
        title: "Λεξικό του Andy",
        search_label: "Αναζήτηση\u00A0:",
        from_label: "Από\u00A0:",
        to_label: "Σε\u00A0:",
        display_label: "Γλώσσα εμφάνισης\u00A0:",
        search_button: "ΑΝΑΖΗΤΗΣΗ 🔍",
        search_results: 'Αποτελέσματα αναζήτησης για «\u00A0{{search_term}}\u00A0»',
        language_label: "Γλώσσα\u00A0:",
        no_results: "Δεν βρέθηκαν αποτελέσματα.",
        please_enter: "Παρακαλώ εισάγετε εδώ έναν όρο αναζήτησης..."
    },
    it: {
        title: "App dizionario di Andy",
        search_label: "Cerca:",
        from_label: "Da:",
        to_label: "A:",
        display_label: "Lingua di visualizzazione:",
        search_button: "CERCA 🔍",
        search_results: 'Risultati della ricerca per "{{search_term}}"',
        language_label: "Lingua:",
        no_results: "Nessun risultato trovato.",
        please_enter: "Inserisci qui un termine di ricerca..."
    },
    pl: {
        title: "Aplikacja słownikowa Andy’ego",
        search_label: "Szukaj:",
        from_label: "Z:",
        to_label: "Na:",
        display_label: "Język interfejsu:",
        search_button: "SZUKAJ 🔍",
        search_results: 'Wyniki wyszukiwania dla „{{search_term}}”',
        language_label: "Język:",
        no_results: "Nie znaleziono wyników.",
        please_enter: "Proszę wprowadzić tutaj wyszukiwane hasło..."
    },
    pt: {
        title: "Aplicativo de dicionário do Andy",
        search_label: "Pesquisar:",
        from_label: "De:",
        to_label: "Para:",
        display_label: "Idioma de exibição:",
        search_button: "PESQUISAR 🔍",
        search_results: 'Resultados da pesquisa para "{{search_term}}"',
        language_label: "Idioma:",
        no_results: "Nenhum resultado encontrado.",
        please_enter: "Por favor insira aqui um termo de pesquisa..."
    },
    ru: {
        title: "Словарь Энди",
        search_label: "Поиск\u00A0:",
        from_label: "С\u00A0:",
        to_label: "На\u00A0:",
        display_label: "Язык интерфейса\u00A0:",
        search_button: "ПОИСК 🔍",
        search_results: 'Результаты поиска для «\u00A0{{search_term}}\u00A0»',
        language_label: "Язык\u00A0:",
        no_results: "Ничего не найдено.",
        please_enter: "Пожалуйста, введите здесь поисковый запрос..."
    },
    sl: {
        title: "Andijeva slovarska aplikacija",
        search_label: "Iskanje:",
        from_label: "Iz:",
        to_label: "V:",
        display_label: "Jezik prikaza:",
        search_button: "IŠČI 🔍",
        search_results: 'Rezultati iskanja za "{{search_term}}"',
        language_label: "Jezik:",
        no_results: "Ni zadetkov.",
        please_enter: "Vnesite iskalni izraz tukaj..."
    },
    tr: {
        title: "Andy'nin Sözlük Uygulaması",
        search_label: "Ara:",
        from_label: "Kaynak:",
        to_label: "Hedef:",
        display_label: "Görüntüleme dili:",
        search_button: "ARA 🔍",
        search_results: '"{{search_term}}" için arama sonuçları',
        language_label: "Dil:",
        no_results: "Sonuç bulunamadı.",
        please_enter: "Lütfen buraya bir arama terimi girin..."
    },
    zh: {
        title: "安迪的词典应用",
        search_label: "搜索：",
        from_label: "源语言：",
        to_label: "目标语言：",
        display_label: "显示语言：",
        search_button: "搜索 🔍",
        search_results: "“{{search_term}}” 的搜索结果",
        language_label: "语言：",
        no_results: "未找到结果。",
        please_enter: "请在此输入搜索词..."
    }
};

const displaySelector = document.querySelector('select[name="display_language"]');
const searchInput = document.querySelector('input[name="search_term"]');

function updateDisplayLanguage(lang) {
    document.querySelectorAll('[data-i18n-key]').forEach(el => {
        const key = el.getAttribute('data-i18n-key');
        if (translations[lang] && translations[lang][key]) {
            let text = translations[lang][key];
            text = text.replace("{{search_term}}", searchInput.value || "");

            if (el.tagName === "INPUT") {
                el.placeholder = text;
            } else if (el.tagName === "TITLE") {
                document.title = text;
            } else {
                el.innerHTML = text;
            }
        }
    });
}

// Initialize on page load
updateDisplayLanguage(displaySelector.value);

// Update when dropdown changes
displaySelector.addEventListener('change', () => {
    updateDisplayLanguage(displaySelector.value);
});
