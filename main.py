import os
try:
    import pyperclip
    CLIPBOARD_ENABLED = True
except ImportError:
    CLIPBOARD_ENABLED = False

from scraper import scraper, downloader, loader
from trainer import trainer, generator

BOOKS_FOLDER = "Books"
MODEL_FOLDER = "Trained_Models"

def download_book_prompt():
    while True:
        book_name = input("Enter a book name to search (or 'q' to cancel): ").strip()
        if book_name.lower() == 'q':
            return False

        results = scraper(book_name)
        if not results:
            print("No books found. Try again.")
            continue

        print("\nAvailable results:")
        for i, (title, _) in enumerate(results, 1):
            print(f"{i}. {title}")
        print("R. Retry search")

        selection = input("Select a book number to download: ").strip()
        if selection.lower() == 'r':
            continue
        if not selection.isdigit() or not (1 <= int(selection) <= len(results)):
            print("Invalid selection.")
            continue

        title, book_id = results[int(selection) - 1]
        return downloader(book_id, title)

def book_selection():
    while True:
        books = loader()
        if not books:
            print("No books found. Please download one.")
            if not download_book_prompt():
                continue
            books = loader()

        print("\nAvailable books:")
        for i, book in enumerate(books, 1):
            print(f"{i}. {book}")
        print("R. Retry search")

        choice = input("Select a book by number: ").strip()
        if choice.lower() == 'r':
            if not download_book_prompt():
                continue
        elif choice.isdigit() and 1 <= int(choice) <= len(books):
            selected_book = books[int(choice) - 1]
            path = os.path.join(BOOKS_FOLDER, selected_book)
            model_path = os.path.join(MODEL_FOLDER, f"{os.path.splitext(selected_book)[0]}.pkl")
            return trainer(path, model_path)
        else:
            print("Invalid selection.")

def main_menu():
    model = book_selection()

    while True:
        print("\nMain Menu:")
        print("1. Generate New Haiku")
        print("2. Copy Last Haiku to Clipboard" if CLIPBOARD_ENABLED else "2. Copy (pyperclip not installed)")
        print("3. Change Book (Select or Download)")
        print("4. Exit")

        choice = input("Choose an option [1-4]: ").strip()

        if choice == '1':
            haiku = generator(model)
            print("\nGenerated Haiku:\n")
            print(haiku)
        elif choice == '2':
            if CLIPBOARD_ENABLED and 'haiku' in locals():
                pyperclip.copy(haiku)
                print("Haiku copied to clipboard.")
            else:
                print("Clipboard unavailable or no haiku generated yet.")
        elif choice == '3':
            if not download_book_prompt():
                continue
            model = book_selection()
        elif choice == '4':
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main_menu()
