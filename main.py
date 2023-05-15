import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import psycopg2
import datetime

class LibraryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.isbn_label = QtWidgets.QLabel("ISBN")
        self.isbn_input = QtWidgets.QLineEdit()
        self.author_label = QtWidgets.QLabel("Автор")
        self.author_input = QtWidgets.QLineEdit()
        self.publication_year_label = QtWidgets.QLabel("Год издания")
        self.publication_year_input = QtWidgets.QLineEdit()
        self.title_label = QtWidgets.QLabel("Название книги")
        self.title_input = QtWidgets.QLineEdit()
        self.pages_label = QtWidgets.QLabel("Количество страниц")
        self.pages_input = QtWidgets.QLineEdit()
        self.status_label = QtWidgets.QLabel("Статус")
        self.status_input = QtWidgets.QLineEdit()
        self.reader_id_label = QtWidgets.QLabel("ID читателя")
        self.reader_id_input = QtWidgets.QLineEdit()
        self.reader_name_label = QtWidgets.QLabel("Имя читателя")
        self.reader_name_input = QtWidgets.QLineEdit()
        self.checkout_date_label = QtWidgets.QLabel("Дата выдачи")
        self.checkout_date_input = QtWidgets.QLineEdit(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.return_date_label = QtWidgets.QLabel("Дата возврата")
        self.return_date_input = QtWidgets.QLineEdit()
        self.add_book_button = QtWidgets.QPushButton("Добавить книгу")
        self.add_book_button.clicked.connect(self.add_book)

        # Set up the layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.isbn_label, 0, 0)
        layout.addWidget(self.isbn_input, 0, 1)
        layout.addWidget(self.author_label, 1, 0)
        layout.addWidget(self.author_input, 1, 1)
        layout.addWidget(self.publication_year_label, 2, 0)
        layout.addWidget(self.publication_year_input, 2, 1)
        layout.addWidget(self.title_label, 3, 0)
        layout.addWidget(self.title_input, 3, 1)
        layout.addWidget(self.pages_label, 4, 0)
        layout.addWidget(self.pages_input, 4, 1)
        layout.addWidget(self.status_label, 5, 0)
        layout.addWidget(self.status_input, 5, 1)
        layout.addWidget(self.reader_id_label, 6, 0)
        layout.addWidget(self.reader_id_input, 6, 1)
        layout.addWidget(self.reader_name_label, 7, 0)
        layout.addWidget(self.reader_name_input, 7, 1)
        layout.addWidget(self.checkout_date_label, 8, 0)
        layout.addWidget(self.checkout_date_input, 8, 1)
        layout.addWidget(self.return_date_label, 9, 0)
        layout.addWidget(self.return_date_input, 9, 1)
        layout.addWidget(self.add_book_button, 10, 0, 1, 2)

        # Set up the database connection
        self.conn = psycopg2.connect(dbname="mylibrary", user="postgres", password="witcher3", host="localhost", port="5432")
        self.cur = self.conn.cursor()

    def add_book(self):
        # Get the book information from the input fields
        isbn = self.isbn_input.text()
        author = self.author_input.text()
        publication_year = self.publication_year_input.text()
        title = self.title_input.text()
        pages = self.pages_input.text()
        status = self.status_input.text()
        reader_id = self.reader_id_input.text()
        reader_name = self.reader_name_input.text()
        checkout_date = self.checkout_date_input.text()
        return_date = self.return_date_input.text()

        # Check if required fields are filled in
        if not (isbn and title):
            QMessageBox.warning(self, "Ошибка", "Поля ISBN и Название книги должны быть заполнены")
            return

        # Insert the book into the database
        try:
            self.cur.execute(
                "INSERT INTO books (isbn, author, publication_year, title, pages, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (isbn, author, publication_year, title, pages, status))
            self.conn.commit()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при добавлении книги в базу данных:\n{str(e)}")
            return

        # If a reader ID is provided, add a checkout record for the book
        if reader_id:
            try:
                self.cur.execute(
                    "INSERT INTO checkouts (isbn, reader_id, checkout_date, return_date) VALUES (%s, %s, %s, %s)",
                    (isbn, reader_id, checkout_date, return_date))
                self.conn.commit()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка",
                                    f"Ошибка при добавлении записи о выдаче книги в базу данных:\n{str(e)}")
                return
        if not isbn:
            error_message = "Введите ISBN книги"
        elif not title:
            error_message = "Введите название книги"
        elif not author:
            error_message = "Введите автора книги"
        elif not publication_year:
            error_message = "Введите год издания книги"
        elif not pages:
            error_message = "Введите количество страниц книги"
        elif not status:
            error_message = "Введите статус книги"
        elif not reader_id and status.lower() == "выдана":
            error_message = "Введите ID читателя"
        elif not reader_name and status.lower() == "выдана":
            error_message = "Введите имя читателя"
        elif not checkout_date and status.lower() == "выдана":
            error_message = "Введите дату выдачи книги"
        elif not return_date and status.lower() == "выдана":
            error_message = "Введите дату возврата книги"
        if error_message:
            self.show_error_message(error_message)
        else:
            # Add the book to the database
            self.cur.execute(
                "INSERT INTO books (isbn, title, author, publication_year, pages, status, reader_id, reader_name, checkout_date, return_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (isbn, title, author, publication_year, pages, status, reader_id, reader_name, checkout_date,
                 return_date),
            )
            self.conn.commit()

            # Show a success message
            success_message = "Книга успешно добавлена"
            self.show_success_message(success_message)

        def show_error_message(self, message):
            """Show an error message."""
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(message)
            msg.setWindowTitle("Ошибка")
            msg.exec_()

        def show_success_message(self, message):
            """Show a success message."""
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle("Успешно")
            msg.exec_()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
