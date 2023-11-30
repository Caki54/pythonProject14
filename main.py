import requests
import re
import spacy
import matplotlib.pyplot as plt

# Adresy URL książek jako słownik z tytułami jako klucze
book_urls = {
    "Pan Tadeusz": "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt",
    "Lalka Tom Pierwszy": "https://wolnelektury.pl/media/book/txt/lalka-tom-pierwszy.txt",
    "Calineczka": "https://wolnelektury.pl/media/book/txt/calineczka.txt",
    "Zemsta": "https://wolnelektury.pl/media/book/txt/zemsta.txt",
    "Syzyfowe prace": "https://wolnelektury.pl/media/book/txt/syzyfowe-prace.txt"
}

# Pobieranie tekstu z URL
def get_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        text_without_digits = re.sub(r'\d', '', text)
        return text_without_digits
    else:
        return ""

# Pobranie i przetworzenie tekstów
corpus = {title: get_text(url) for title, url in book_urls.items()}

# # Pobranie listy polskich stopwords z GitHuba
# url_stopwords = 'https://raw.githubusercontent.com/bieli/stopwords/master/polish.stopwords.txt'
# response = requests.get(url_stopwords)
# custom_stopwords = set(response.text.splitlines())

# Załadowanie polskiego modelu
nlp = spacy.load('pl_core_news_md')

# Analiza części mowy
def analyze_pos(corpus):
    pos_results = {}
    for title, text in corpus.items():
        doc = nlp(text)
        pos_count = {}
        for token in doc:
            if token.pos_ in pos_count:
                pos_count[token.pos_] += 1
            else:
                pos_count[token.pos_] = 1
        pos_results[title] = pos_count
    return pos_results

# Wywołanie funkcji analizy
pos_analysis = analyze_pos(corpus)

# Wizualizacja częstości występowania klas gramatycznych
def plot_pos_counts(pos_analysis):
    for title, pos_counts in pos_analysis.items():
        plt.figure(figsize=(10, 6))
        plt.bar(pos_counts.keys(), pos_counts.values(), color='blue')
        plt.xlabel('Parts of Speech')
        plt.ylabel('Counts')
        plt.title(f'POS Frequency in {title}')
        plt.xticks(rotation=45)
        plt.show()

# Wywołanie funkcji wizualizacji
plot_pos_counts(pos_analysis)