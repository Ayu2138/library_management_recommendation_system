import csv
import os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.csv")

FIELDS = ["book_id", "title", "edition", "author", "genre",
          "status", "times_issued", "issue_date"]


# Load books from CSV
def load_books():
    books = []

    if os.path.exists(FILE):
        with open(FILE, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Skip empty rows and make sure all required fields exist
                if row.get("title"):
                    for field in FIELDS:
                        if field not in row or row[field] is None:
                            row[field] = ""
                    books.append(row)

    return books


# Save books to CSV
def save_books(books):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)


# Find a book using its title (case-insensitive)
def find_book(books, title):
    for book in books:
        if book["title"].strip().lower() == title.strip().lower():
            return book
    return None


# Display book details
def show_book(book):
    print("\\nBook ID:", book["book_id"])
    print("Title:", book["title"])
    print("Edition:", book["edition"])
    print("Author:", book["author"])
    print("Genre:", book["genre"])
    print("Status:", book["status"])


# Add a book
def add_book():
    books = load_books()

    title = input("Enter title: ").strip()
    edition = input("Enter edition: ").strip()
    author = input("Enter author: ").strip()
    genre = input("Enter genre: ").strip()

    if not title or not edition.isdigit() or int(edition) < 1 or not author or not genre:
        print("Invalid details.")
        return

    if find_book(books, title):
        print("Book already exists.")
        return

    book_id = 1
    for book in books:
        if book["book_id"].isdigit() and int(book["book_id"]) >= book_id:
            book_id = int(book["book_id"]) + 1

    new_book = {
        "book_id": str(book_id),
        "title": title,
        "edition": edition,
        "author": author,
        "genre": genre,
        "status": "Available",
        "times_issued": "0",
        "issue_date": ""
    }

    books.append(new_book)
    save_books(books)
    print("Book added successfully.")


# View all books
def view_books():
    books = load_books()

    if not books:
        print("No books available.")
        return

    for book in books:
        show_book(book)


# Search books by partial title
def search_book():
    books = load_books()
    name = input("Enter book name: ").strip().lower()

    found = False
    for book in books:
        if name in book["title"].lower():
            show_book(book)
            found = True

    if not found:
        print("Book not found.")


# Update a book using its title
def update_book():
    books = load_books()
    name = input("Enter book name to update: ").strip()
    book = find_book(books, name)

    if book is None:
        print("Book not found.")
        return

    new_title = input("New title (press Enter to keep current): ").strip()
    new_edition = input("New edition (press Enter to keep current): ").strip()
    new_author = input("New author (press Enter to keep current): ").strip()
    new_genre = input("New genre (press Enter to keep current): ").strip()

    if new_edition and (not new_edition.isdigit() or int(new_edition) < 1):
        print("Invalid edition. Update cancelled.")
        return

    if new_title:
        # Avoid changing the title to one already used by another book
        other_book = find_book(books, new_title)
        if other_book is not None and other_book is not book:
            print("Another book already has that title.")
            return
        book["title"] = new_title

    if new_edition:
        book["edition"] = new_edition
    if new_author:
        book["author"] = new_author
    if new_genre:
        book["genre"] = new_genre

    save_books(books)
    print("Book updated successfully.")


# Delete a book using its title
def delete_book():
    books = load_books()

    if not books:
        print("No books available.")
        return

    name = input("Enter book name to delete: ").strip()
    book = find_book(books, name)

    if book is None:
        print("Book not found.")
        return

    confirm = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
    if confirm == "y":
        books.remove(book)
        save_books(books)
        print("Book deleted successfully.")
    else:
        print("Delete cancelled.")


# Issue a book using its title
def issue_book():
    books = load_books()
    name = input("Enter book name to issue: ").strip()
    book = find_book(books, name)

    if book is None:
        print("Book not found.")
        return

    if book["status"].strip().lower() == "issued":
        print("Book is already issued.")
        return

    book["status"] = "Issued"
    try:
        book["times_issued"] = str(int(book["times_issued"] or 0) + 1)
    except ValueError:
        book["times_issued"] = "1"

    save_books(books)
    print("Book issued successfully.")


# Return a book using its title
def return_book():
    books = load_books()
    name = input("Enter book name to return: ").strip()
    book = find_book(books, name)

    if book is None:
        print("Book not found.")
        return

    if book["status"].strip().lower() == "available":
        print("Book is already available.")
        return

    book["status"] = "Available"
    save_books(books)
    print("Book returned successfully.")


# Generate a simple report
def report():
    books = load_books()

    if not books:
        print("No books available.")
        return

    genre_count = {}
    available = 0
    issued = 0

    for book in books:
        genre = book["genre"]
        genre_count[genre] = genre_count.get(genre, 0) + 1

        if book["status"].strip().lower() == "available":
            available += 1
        else:
            issued += 1

    print("\\nBooks by genre:")
    for genre, count in genre_count.items():
        print(genre, ":", count)

    print("\\nTotal books:", len(books))
    print("Available:", available)
    print("Issued:", issued)


# Main menu
def main():
    while True:
        print("\\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add book")
        print("2. View books")
        print("3. Search book")
        print("4. Update book")
        print("5. Delete book")
        print("6. Issue book")
        print("7. Return book")
        print("8. Generate report")
        print("9. Exit")

        choice = input("\\nEnter choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            issue_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            report()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 to 9.")


if __name__ == "__main__":
    main()