import csv, os

FILE = "books.csv"
FIELDS = ["book_id", "title", "edition", "author", "genre", "status", "times_issued"]

def load_books():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="") as f:
        return list(csv.DictReader(f))

def save_books(books):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)

def add_book():
    books = load_books()
    title = input("Title: ").strip()
    edition = input("Edition: ").strip()
    author = input("Author: ").strip()
    genre = input("Genre: ").strip().title()
    if not (title and author and genre) or not edition.isdigit():
        print("Invalid input. Title, author, genre required; edition must be a number.")
        return
    for b in books:
        if (b["title"].lower(), b["edition"], b["author"].lower()) == (title.lower(), edition, author.lower()):
            print("This book already exists.")
            return
    book_id = str(len(books) + 1)
    books.append({"book_id": book_id, "title": title, "edition": edition,
                  "author": author, "genre": genre, "status": "Available", "times_issued": "0"})
    save_books(books)
    print("Book added.")

def search_books():
    books = load_books()
    print("Search by: 1) Title  2) Author  3) Genre")
    choice = input("Choice: ").strip()
    keys = {"1": "title", "2": "author", "3": "genre"}
    if choice not in keys:
        print("Invalid choice.")
        return
    term = input("Search for: ").strip().lower()
    if not term:
        print("Search term cannot be empty.")
        return
    matches = [b for b in books if term in b[keys[choice]].lower()]
    if not matches:
        print("No books found.")
        return
    for b in matches:
        print(f"{b['book_id']}. {b['title']} (Ed. {b['edition']}) by {b['author']} "
              f"[{b['genre']}] - {b['status']}")

def issue_book():
    books = load_books()
    book_id = input("Book ID to issue: ").strip()
    for b in books:
        if b["book_id"] == book_id:
            if b["status"] == "Issued":
                print("Book is already issued.")
                return
            b["status"] = "Issued"
            b["times_issued"] = str(int(b["times_issued"]) + 1)
            save_books(books)
            print(f"Issued: {b['title']}")
            return
    print("Book ID not found.")

def return_book():
    books = load_books()
    book_id = input("Book ID to return: ").strip()
    for b in books:
        if b["book_id"] == book_id:
            if b["status"] == "Available":
                print("This book was not issued.")
                return
            b["status"] = "Available"
            save_books(books)
            print(f"Returned: {b['title']}")
            return
    print("Book ID not found.")

def report():
    books = load_books()
    if not books:
        print("No books to report on.")
        return

    # 1. Books per genre
    genre_count = {}
    for b in books:
        genre_count[b["genre"]] = genre_count.get(b["genre"], 0) + 1
    print("\nBooks per genre:")
    for genre, count in sorted(genre_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {genre}: {count}")

    # 2. Most issued books (top 3)
    ranked = sorted(books, key=lambda b: int(b["times_issued"]), reverse=True)[:3]
    print("\nMost issued books:")
    for i, b in enumerate(ranked, 1):
        print(f"  {i}. {b['title']} - {b['times_issued']} times")

    # 3. Availability summary
    issued = sum(1 for b in books if b["status"] == "Issued")
    print(f"\nTotal: {len(books)} | Available: {len(books) - issued} | Issued: {issued}")

def main():
    menu = {"1": add_book, "2": search_books, "3": issue_book,
            "4": return_book, "5": report}
    while True:
        print("\n1.Add  2.Search  3.Issue  4.Return  5.Report  6.Exit")
        choice = input("Choice: ").strip()
        if choice == "6":
            break
        menu.get(choice, lambda: print("Invalid choice."))()

main()