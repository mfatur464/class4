from datetime import datetime
from typing import List


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False  

    def return_book(self) -> None:
        """Mengembalikan status buku menjadi tersedia"""
        if self.is_borrowed:
            self.is_borrowed = False
            print(f"Buku '{self.title}' telah dikembalikan.")
        else:
            print(f"Buku '{self.title}' tidak sedang dipinjam.")

    def __str__(self):
        status = "Dipinjam" if self.is_borrowed else "Tersedia"
        return f"Book(title='{self.title}', author='{self.author}', isbn={self.isbn}, status={status})"


class Member:
    def __init__(self, name: str, member_id: str):
        self.name = name
        self.member_id = member_id
        self.borrowed_books: List[BorrowTransaction] = []  

    def borrow_book(self, book: 'Book', staff: 'Staff') -> None:
        """Anggota meminjam buku melalui staff"""
        if book.is_borrowed:
            print(f"Buku '{book.title}' sedang dipinjam oleh orang lain.")
            return
        
        transaction = BorrowTransaction(book, self, staff)
        transaction.borrow_book()
        
        self.borrowed_books.append(transaction)
        book.is_borrowed = True
        print(f"{self.name} berhasil meminjam buku '{book.title}'")

    def return_book(self, book: 'Book', staff: 'Staff') -> None:
        """Anggota mengembalikan buku melalui staff"""
        for transaction in self.borrowed_books:
            if transaction.book == book and not transaction.returned:
                transaction.return_book(staff)
                book.is_borrowed = False
                print(f"{self.name} berhasil mengembalikan buku '{book.title}'")
                return
        
        print(f"{self.name} tidak meminjam buku '{book.title}' atau buku sudah dikembalikan.")

    def list_borrowed_books(self) -> None:
        if not self.borrowed_books:
            print(f"{self.name} belum meminjam buku apapun.")
            return
            
        print(f"Daftar buku yang dipinjam oleh {self.name}:")
        for trans in self.borrowed_books:
            if not trans.returned:
                print(f"  - {trans.book.title} (dipinjam pada: {trans.borrow_date})")

    def __str__(self):
        return f"Member(name='{self.name}', member_id={self.member_id}, borrowed_count={len([t for t in self.borrowed_books if not t.returned])})"


class Staff:
    def __init__(self, name: str, staff_id: str):
        self.name = name
        self.staff_id = staff_id

    def __str__(self):
        return f"Staff(name='{self.name}', staff_id={self.staff_id})"


class BorrowTransaction:
    def __init__(self, book: Book, member: Member, staff: Staff):
        self.book = book
        self.member = member
        self.staff = staff
        self.borrow_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.returned: bool = False  # state: apakah sudah dikembalikan atau belum

    def borrow_book(self) -> None:
        """Proses peminjaman buku"""
        if self.book.is_borrowed:
            raise ValueError("Buku sudah dipinjam")
        self.book.is_borrowed = True
        self.returned = False
        print(f"Transaksi peminjaman dicatat oleh {self.staff.name} pada {self.borrow_date}")

    def return_book(self, staff: Staff) -> None:
        """Proses pengembalian buku"""
        if self.returned:
            print("Buku sudah pernah dikembalikan sebelumnya.")
            return
            
        self.returned = True
        self.book.is_borrowed = False
        print(f"Pengembalian dicatat oleh {staff.name} pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def __str__(self):
        status = "Sudah dikembalikan" if self.returned else "Masih dipinjam"
        return (f"Transaction(book={self.book.title}, member={self.member.name}, "
                f"staff={self.staff.name}, date={self.borrow_date}, status={status})")



if __name__ == "__main__":

    book1 = Book("Pemrograman Python", "Guido van Rossum", "978-1234567890")
    book2 = Book("Clean Code", "Robert C. Martin", "978-9876543210")

    member1 = Member("Budi Santoso", "MBR001")
    staff1 = Staff("Ibu Ani", "STF101")

    print(book1)
    print(member1)
    print(staff1)

    print("\n=== Proses Peminjaman ===")
    member1.borrow_book(book1, staff1)
    member1.borrow_book(book2, staff1)

    member1.list_borrowed_books()

    print("\n=== Status buku setelah dipinjam ===")
    print(book1)
    print(book2)

    print("\n=== Proses Pengembalian ===")
    member1.return_book(book1, staff1)

    print("\n=== Daftar buku yang masih dipinjam ===")
    member1.list_borrowed_books()

    print("\n=== Status akhir ===")
    print(book1)
    print(book2)