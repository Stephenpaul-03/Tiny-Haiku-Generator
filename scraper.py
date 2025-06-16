import os
import re
import requests
from bs4 import BeautifulSoup
from gutenberg_cleaner import simple_cleaner

BOOKS_FOLDER = "Books"
os.makedirs(BOOKS_FOLDER, exist_ok=True)

def scraper(book_name):
    search_url = f"https://www.gutenberg.org/ebooks/search/?query={book_name.replace(' ', '+')}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print("Failed to retrieve the search results.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    book_links = soup.find_all('li', class_='booklink')
    books = []
    titles_seen = set()

    for link in book_links:
        title_tag = link.find('span', class_='title')
        if title_tag:
            title = title_tag.text.strip()
            if title.lower() not in titles_seen:
                book_id = link.find('a')['href'].split('/')[-1]
                books.append((title, book_id))
                titles_seen.add(title.lower())
            if len(books) >= 5:
                break

    return books

def downloader(book_id, book_name):
    book_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
    response = requests.get(book_url)
    if response.status_code == 200:
        raw_filename = os.path.join(BOOKS_FOLDER, f"{book_name}_raw.txt")
        with open(raw_filename, 'w', encoding='utf-8') as raw_file:
            raw_file.write(response.text)

        cleaned_content = simple_cleaner(response.text)
        cleaned_filename = os.path.join(BOOKS_FOLDER, f"{book_name}.txt")
        with open(cleaned_filename, 'w', encoding='utf-8') as clean_file:
            clean_file.write(cleaned_content)

        print(f"Book downloaded and cleaned: {cleaned_filename}")
        return True
    else:
        print("Download failed.")
        return False

def loader():
    return [f for f in os.listdir(BOOKS_FOLDER) if f.endswith(".txt") and not f.endswith("_raw.txt")]

def reader(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()
