import csv


class Book:
    def __init__(self, title: str, author: str, isbn: int, availability_status: bool):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.availability_status = availability_status

    @classmethod
    # receives class reference as first argument
    def instantiate_from_csv(cls):
        with open('bookRecord.csv', 'r') as f:
            reader = csv.DictReader(f)
            bookRecord = list(reader)

        for book in bookRecord:
            Book(
                title=book.get('title'),
                author=book.get('book'),
                isbn=book.get('isbn'),
                availability_status=book.get('availability_status')
            )


class Library(Book):
    def __init__(self, title: str, author: str, isbn: int, availability_status: bool):

        super().__init__(
            title, author, isbn, availability_status
        )

    def search_books(self):
        print(f'''Book details
Title: {self.title}
Author: {self.author}
ISBN: {self.isbn}
Availability Status: {self.availability_status}\n''')

    @staticmethod
    def add_books(book):
        with open('bookRecord.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([book.title, book.author, book.isbn, book.availability_status])

    @staticmethod
    def remove_books(book_title):
        books = []

        # opens csv file in read mode
        with open('bookRecord.csv', 'r') as f:
            # csv.reader(f) creates a CSV reader object to iterate over the rows of the CSV file
            reader = csv.reader(f)
            # reads each row and filters out the rows where the first column matches book_title
            # All rows that do not match the given book title are added to the books list.
            books = [row for row in reader if row[0] != book_title]

        # opens csv file in write mode
        with open('bookRecord.csv', 'w', newline='') as f:
            # creates a CSV writer object to write rows to the CSV file
            writer = csv.writer(f)
            # writes all the rows stored in the books list back to the CSV file
            writer.writerows(books)


class Member():
    def __init__(self, name: int, member_id: int, borrowed_books: list):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = borrowed_books

    def lend_books(self, book_title):
        borrowed_books = []
        book_found = False
        with open('bookRecord.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['title'] == book_title:
                    if row['availability_status'] == 'True':
                        row['availability_status'] = 'False'
                        self.borrowed_books.append(book_title)
                        book_found = True
                        print(f"Book '{book_title}' has been borrowed by {self.name}!\n")
                    else:
                        print(f"Book '{book_title}' is not available!")
                borrowed_books.append(row)
        if book_found:
            # opens file in write mode
            with open('bookRecord.csv', 'w', newline='') as f:
                # fieldnames list specifies the order and the names of the columns in the CSV file
                fieldnames = ['title', 'author', 'isbn', 'availability_status']
                # The DictWriter object is responsible for writing dictionaries to the CSV file
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # The writeheader method writes a row of column headers to the CSV file
                writer.writeheader()
                # writes all the rows stored in the borrowed_books list back to the CSV file.
                # writes borrowed books record with changed availability_status if the book was borrowed
                writer.writerows(borrowed_books)

    @staticmethod
    def return_books(book_title):
        returned_books = []
        with open('bookRecord.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['title'] == book_title:
                    row['availability_status'] = 'True'
                    print(f"Book '{book_title}' has been returned!")
                returned_books.append(row)
        with open('bookRecord.csv', 'w', newline='') as f:
            fieldnames = ['title', 'author', 'isbn', 'availability_status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(returned_books)


# Search a book
Book.instantiate_from_csv()
book_from_csv = Library("Kite Runner", "Khalid Hossaini", 1234, True)
book_from_csv.search_books()

# Create a new book instance
new_book1 = Book("Seven Habits", "Stephen Covey", 6097, True)

# Add the new books to the CSV file
Library.add_books(new_book1)

# Borrow a book
member = Member("Aliza", 8, [])
member.lend_books("Quiet")

# Return a book
member.return_books("It Ends With Us")
